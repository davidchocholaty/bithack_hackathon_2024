// ----------  Selecting facilities ----------
// Function to handle the facility row click
function handleFacilityClick(event) {
  // Get the clicked element
  const clickedElement = event.currentTarget;

  // Check if the clicked element has the active class
  if (clickedElement.classList.contains("active")) {
    // If it has the active class, do nothing
    return;
  }

  // Find the currently active element
  const currentActive = document.querySelector(".facility-row.active");

  // If there is a currently active element, remove its active class
  if (currentActive) {
    currentActive.classList.remove("active");
  }

  // Add the active class to the clicked element
  clickedElement.classList.add("active");

  // Fetch facility data from the backend
  const facilityId = clickedElement.dataset.facilityId; // Make sure to add this data attribute
  fetch(`/facility/${facilityId}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      updateDashboard(data); // Call the updateDashboard function with the fetched data
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
    });
}

// Function to update the dashboard content based on the clicked facility
function updateDashboard(clickedElement) {
  // Get facility data from the clicked element
  const facilityName = clickedElement.querySelector("h3").innerText;
  const occupiedCount =
    clickedElement.querySelector(".healthbar").dataset.occupied;
  const totalCapacity =
    clickedElement.querySelector(".healthbar").dataset.overall;
  const dayCount = clickedElement.dataset.dayCount; // You will need to include this data in your facility element
  const address = clickedElement.dataset.address; // You will need to include this data in your facility element

  // Calculate occupancy rate
  const occupancyRate = ((occupiedCount / totalCapacity) * 100).toFixed(2);

  // Update the dashboard items with facility data
  document.getElementById(
    "dashboard-heading"
  ).innerText = `${facilityName} Dashboard`;
  document.getElementById("occupied-count").innerText = occupiedCount;
  document.getElementById("total-capacity").innerText = totalCapacity;
  document.getElementById("day-count").innerText = dayCount;
  document.getElementById("facility-address").innerText = address;
  document.getElementById("occupancy-rate").innerText = occupancyRate;
  document.getElementById("facility-name").innerText = facilityName;
}

// Get all facility rows
const facilityRows = document.querySelectorAll(".facility-row");

// Attach the click event listener to each facility row
facilityRows.forEach((row) => {
  row.addEventListener("click", handleFacilityClick);
});

// ----------  Occupancy indicator ----------
// Select all health bars
const healthbars = document.querySelectorAll(".healthbar");

healthbars.forEach((healthbar) => {
  // Get values from data attributes
  const occupancy = parseFloat(healthbar.getAttribute("data-occupied"));
  const total = parseFloat(healthbar.getAttribute("data-overall"));
  const occupancyPercentage = (occupancy / total) * 100;

  // Set health bar color based on occupancy percentage
  if (occupancyPercentage >= 75) {
    healthbar.classList.add("healthbar-danger");
  } else if (occupancyPercentage >= 50) {
    healthbar.classList.add("healthbar-warning");
  } else {
    healthbar.classList.add("healthbar-full");
  }
});
