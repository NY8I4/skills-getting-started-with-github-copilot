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

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
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

        // Populate participants list
        participantsList.innerHTML = '';
        if (details.participants && details.participants.length > 0) {
          details.participants.forEach(email => {
            const li = document.createElement('li');
            li.textContent = email;
            participantsList.appendChild(li);
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

        // Append the new participant to the list
        const activityCardElement = Array.from(activitiesList.children).find(card => {
          const title = card.querySelector('h4');
          return title && title.textContent === activity;
        });

        if (activityCardElement) {
          const participantsList = activityCardElement.querySelector('.participants__list');
          if (participantsList) {
            // remove "No participants yet" placeholder if present
            const empty = participantsList.querySelector('.participants__empty');
            if (empty) empty.remove();
            const li = document.createElement('li');
            li.textContent = email;
            participantsList.appendChild(li);
          }
        }
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
