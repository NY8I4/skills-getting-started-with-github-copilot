"""Tests for the Mergington High School Activities API."""

import pytest


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_redirect(self, client):
        """Test that the root endpoint redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Tests for the GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test that /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9
        assert "Baseball Team" in data
        assert "Basketball Club" in data
        assert "Chess Club" in data
    
    def test_activity_has_required_fields(self, client):
        """Test that each activity has required fields."""
        response = client.get("/activities")
        data = response.json()
        
        activity = data["Baseball Team"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
    
    def test_participants_are_list(self, client):
        """Test that participants field is a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity in data.items():
            assert isinstance(activity["participants"], list)


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_new_participant(self, client):
        """Test signing up a new participant."""
        response = client.post(
            "/activities/Baseball Team/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
    
    def test_signup_updates_participants_list(self, client):
        """Test that signup adds participant to the list."""
        email = "newstudent@mergington.edu"
        client.post(f"/activities/Baseball Team/signup?email={email}")
        
        response = client.get("/activities")
        data = response.json()
        
        assert email in data["Baseball Team"]["participants"]
    
    def test_signup_duplicate_participant_fails(self, client):
        """Test that signing up with the same email twice fails."""
        email = "alex@mergington.edu"
        
        # First signup should fail because alex is already in Baseball Team
        response = client.post(f"/activities/Baseball Team/signup?email={email}")
        assert response.status_code == 400
        
        data = response.json()
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_nonexistent_activity_fails(self, client):
        """Test that signing up for a non-existent activity fails."""
        response = client.post(
            "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_signup_full_activity_fails(self, client):
        """Test that signing up for a full activity fails."""
        # Debate Team has max 10 participants and 1 currently (mason@mergington.edu)
        # Fill it up
        for i in range(9):
            email = f"student{i}@mergington.edu"
            client.post(f"/activities/Debate Team/signup?email={email}")
        
        # Now it should be full (10/10)
        response = client.post(
            "/activities/Debate Team/signup?email=lastperson@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "full" in data["detail"].lower()


class TestUnregisterEndpoint:
    """Tests for the DELETE /activities/{activity_name}/participants endpoint."""
    
    def test_unregister_existing_participant(self, client):
        """Test unregistering an existing participant."""
        response = client.delete(
            "/activities/Baseball Team/participants?email=alex@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "Unregistered" in data["message"]
    
    def test_unregister_removes_from_list(self, client):
        """Test that unregister removes participant from the list."""
        email = "alex@mergington.edu"
        client.delete(f"/activities/Baseball Team/participants?email={email}")
        
        response = client.get("/activities")
        data = response.json()
        
        assert email not in data["Baseball Team"]["participants"]
    
    def test_unregister_nonexistent_participant_fails(self, client):
        """Test that unregistering a non-existent participant fails."""
        response = client.delete(
            "/activities/Baseball Team/participants?email=notreal@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_unregister_nonexistent_activity_fails(self, client):
        """Test that unregistering from a non-existent activity fails."""
        response = client.delete(
            "/activities/Nonexistent Activity/participants?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()


class TestIntegration:
    """Integration tests for the API."""
    
    def test_signup_then_unregister_workflow(self, client):
        """Test the full workflow of signing up and then unregistering."""
        email = "workflow_test@mergington.edu"
        activity = "Chess Club"
        
        # Sign up
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify signup
        response = client.get("/activities")
        data = response.json()
        assert email in data[activity]["participants"]
        
        # Unregister
        response = client.delete(f"/activities/{activity}/participants?email={email}")
        assert response.status_code == 200
        
        # Verify unregister
        response = client.get("/activities")
        data = response.json()
        assert email not in data[activity]["participants"]
    
    def test_multiple_signups_different_activities(self, client):
        """Test signing up for multiple different activities."""
        email = "multi_activity@mergington.edu"
        activities = ["Art Studio", "Drama Club", "Science Club"]
        
        for activity in activities:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all signups
        response = client.get("/activities")
        data = response.json()
        
        for activity in activities:
            assert email in data[activity]["participants"]
