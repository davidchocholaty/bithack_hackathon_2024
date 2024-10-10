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

  //   console.log(facilityId);
  fetch(`facility/${facilityId}/`)
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
function updateDashboard(data) {
  // Check if data is an object and has the expected properties
  if (typeof data !== "object" || data === null) {
    console.error("Invalid data format:", data);
    return; // Exit if data is not valid
  }
  console.log(data);

  // Safeguard access to facility and chart_data
  let facility = data.facility;
//   const chartData = data.facility.chart_data;

  console.log(facility);
  console.log(chartData);
  if (!facility || !chartData) {
    facility = data;
    // console.error("Missing facility or chart data:", data);
    // return; // Exit if facility or chart data is missing
  }

  // Get facility data from the fetched JSON
  const facilityName = facility.name;
  const occupiedCount = facility.count;
  const totalCapacity = facility.capacity;
  const dayCount = facility.day_count;
  const address = facility.address;

  // Calculate occupancy rate
  const occupancyRate = ((occupiedCount / totalCapacity) * 100).toFixed(2);

  // Update the dashboard heading with the facility name
  document.getElementById("dashboard-heading").innerText = `${facilityName}`;

  // Update the dashboard items with facility data
  // Check and update each element if it exists
  const dashboardHeading = document.getElementById("dashboard-heading");
  if (dashboardHeading) {
    dashboardHeading.innerText = `${facilityName} Dashboard`;
  }

  const occupiedCountElem = document.getElementById("occupied-count");
  if (occupiedCountElem) {
    occupiedCountElem.innerText = occupiedCount;
  }

  const totalCapacityElem = document.getElementById("total-capacity");
  if (totalCapacityElem) {
    totalCapacityElem.innerText = totalCapacity;
  }

  const dayCountElem = document.getElementById("day-count");
  if (dayCountElem) {
    dayCountElem.innerText = dayCount;
  }

  const addressElem = document.getElementById("facility-address");
  if (addressElem) {
    addressElem.innerText = address;
  }

  const occupancyRateElem = document.getElementById("occupancy-rate");
  if (occupancyRateElem) {
    occupancyRateElem.innerText = occupancyRate;
  }

  const facilityNameElem = document.getElementById("facility-name");
  if (facilityNameElem) {
    facilityNameElem.innerText = facilityName;
  }

//   if (chartData) {
//     updateChart(chartData);
//   }
}

// Function to update the chart using chart_data from the JSON response
function updateChart(chartData) {
  const ctx = document.getElementById("occupancyChart").getContext("2d");

  // Assuming you are using Chart.js, you need to check if the chart already exists
  if (window.occupancyChart) {
    // If chart already exists, update it
    window.occupancyChart.data.labels = chartData.labels;
    window.occupancyChart.data.datasets[0].data = chartData.values;
    window.occupancyChart.update();
  } else {
    // If the chart doesn't exist yet, create a new one
    window.occupancyChart = new Chart(ctx, {
      type: "line", // You can adjust the type of chart as per your requirement
      data: {
        labels: chartData.labels,
        datasets: [
          {
            label: "Median Occupancy per Hour",
            data: chartData.values,
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
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
