document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message and reset activity select
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4 class="activity-name">${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        // Participants section
        let participantsList = activityCard.querySelector('.participants__list');
        if (!participantsList) {
          // If card is built purely in JS, create the section:
          const participantsSection = document.createElement('div');
          participantsSection.className = 'participants';
          const pTitle = document.createElement('h4');
          pTitle.className = 'participants__title';
          pTitle.textContent = 'Participants';
          participantsList = document.createElement('ul');
          participantsList.className = 'participants__list';
          participantsSection.appendChild(pTitle);
          participantsSection.appendChild(participantsList);
          activityCard.appendChild(participantsSection);
        }

        // Helper to create a participant list item with delete button
        function createParticipantListItem(email) {
          const li = document.createElement('li');
          li.className = 'participants__item';

          const span = document.createElement('span');
          span.className = 'participant__email';
          span.textContent = email;

          const btn = document.createElement('button');
          btn.className = 'participant__remove';
          btn.setAttribute('aria-label', `Remove ${email}`);
          btn.innerHTML = '&#10005;';

          btn.addEventListener('click', async (e) => {
            e.preventDefault();
            // Call DELETE endpoint
            try {
              const res = await fetch(
                `/activities/${encodeURIComponent(name)}/participants?email=${encodeURIComponent(email)}`,
                { method: 'DELETE' }
              );
              const data = await res.json();
              if (res.ok) {
                // remove list item
                li.remove();
                // if list empty, show placeholder
                if (!participantsList.querySelector('.participants__item')) {
                  const placeholder = document.createElement('li');
                  placeholder.className = 'participants__empty';
                  placeholder.textContent = 'No participants yet';
                  participantsList.appendChild(placeholder);
                }
              } else {
                console.error('Failed to remove participant', data);
                alert(data.detail || 'Failed to remove participant');
              }
            } catch (err) {
              console.error('Error removing participant', err);
              alert('Failed to remove participant');
            }
          });

          li.appendChild(span);
          li.appendChild(btn);
          return li;
        }

        // Populate participants list
        participantsList.innerHTML = '';
        if (details.participants && details.participants.length > 0) {
          details.participants.forEach(email => {
            participantsList.appendChild(createParticipantListItem(email));
          });
        } else {
          const li = document.createElement('li');
          li.textContent = 'No participants yet';
          li.className = 'participants__empty';
          participantsList.appendChild(li);
        }

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();

        // Refresh activities list so availability and participants are up-to-date
        await fetchActivities();

      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
