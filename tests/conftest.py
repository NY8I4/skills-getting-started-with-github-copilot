"""Pytest configuration and fixtures for testing the FastAPI app."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    from src.app import activities
    
    # Store initial state
    initial_activities = {
        "Baseball Team": {
            "description": "Join our competitive baseball team and compete in regional tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Play basketball and develop teamwork skills",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["james@mergington.edu", "sophia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Compete in debate competitions and improve argumentation skills",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["mason@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["ethan@mergington.edu", "charlotte@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(initial_activities)
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(initial_activities)
