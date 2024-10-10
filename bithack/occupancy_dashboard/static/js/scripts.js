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
  const facilityId = clickedElement.getAttribute("data-facility-id");

  console.log(facilityId);
  fetch(`facility/${facilityId}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
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
function updateDashboard(data) {
  // Check if data is an object and has the expected properties
  if (typeof data !== "object" || data === null) {
    console.error("Invalid data format:", data);
    return; // Exit if data is not valid
  }

  // Get facility data from the fetched JSON
  const facilityName = data.name;
  const occupiedCount = data.count;
  const totalCapacity = data.capacity;
  const dayCount = data.day_count;
  const address = data.address;

  // Calculate occupancy rate
  const occupancyRate = ((occupiedCount / totalCapacity) * 100).toFixed(2);

  // Update the dashboard heading with the facility name
  document.getElementById(
    "dashboard-heading"
  ).innerText = `${facilityName} Dashboard`;

  // Update the dashboard items with facility data
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
