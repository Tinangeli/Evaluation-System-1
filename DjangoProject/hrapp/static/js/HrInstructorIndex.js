


async function loadData() {
    try {
        const response = await fetch("http://localhost:8000/api/instructor-data/"); // Fetch from Django API
        const data = await response.json();

        // Store data globally for comboboxes
        window.facultyOptions = data.faculties;
        window.professorOptions = data.professors;
        window.semesterOptions = data.semesters;
        window.schoolYearOptions = data.schoolYears;

        console.log("Data Loaded from Django:", data); // Debugging
    } catch (error) {
        console.error("Error loading data:", error);
    }
}

// Call loadData() when the page loads
document.addEventListener("DOMContentLoaded", function () {
    loadData();
});


function showCombobox(inputId, optionsArray) {
    const inputElement = document.getElementById(inputId);
    const combobox = document.getElementById(inputId + "Combobox");
    const inputValue = inputElement.value.toLowerCase();

    combobox.innerHTML = "";

    if (inputValue) {
        let filteredOptions = optionsArray.filter(option =>
            option.name.toLowerCase().includes(inputValue)  // Search by schedule name
        );

        if (filteredOptions.length > 0) {
            filteredOptions.forEach(option => {
                const div = document.createElement("div");
                div.textContent = option.name;  // Display schedule name
                div.onclick = function () {
                    inputElement.value = option.name;
                    combobox.style.display = "none";
                    fillScheduleFields(option);  // Populate related fields
                };
                combobox.appendChild(div);
            });

            combobox.style.display = "block";
            combobox.style.position = "absolute";
            combobox.style.width = inputElement.offsetWidth + "px";
        } else {
            combobox.style.display = "none";
        }
    } else {
        combobox.style.display = "none";
    }
}
function fillScheduleFields(schedule) {
    document.getElementById("FacultyInput").value = schedule.course__name;
    document.getElementById("ProfessorInput").value = schedule.professor__name;
    document.getElementById("SemesterInput").value = schedule.semester;
    document.getElementById("SchoolYearInput").value = schedule.year;
}
async function loadSchedules() {
    try {
        const response = await fetch("http://localhost:8000/api/instructor-data/");
        const data = await response.json();

        // Store schedules globally
        window.scheduleOptions = data.schedules;

        console.log("Schedules Loaded:", window.scheduleOptions);  // Debugging
    } catch (error) {
        console.error("Error loading schedules:", error);
    }
}

// Load schedules when page loads
document.addEventListener("DOMContentLoaded", function () {
    loadSchedules();
});




async function fetch_instructor_pie_chart_data() {
    try{
        const  response = await fetch("http://localhost:8000/api/instructor-pie-chart/")
        const result = await response.json();

        const labels = result.data.map(item => item.category);
        const scores = result.data.map(item => item.score);

        const data = {
            labels: labels,
            datasets: [{
                data: scores,
                backgroundColor: [
                    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
                    "#9966FF", "#FF9F40", "#FF6384", "#36A2EB",
                    "#FFCE56", "#4BC0C0", "#9966FF"
                ],
                hoverOffset: 20
            }]
        };

        const ctx = document.getElementById("instructor_pie_chart").getContext("2d");
        const instructor_pie_chart = new Chart(ctx, {
            type: "pie",
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: "bottom" } },
                onclick: function (event, elements) {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const category = labels[index]; // Get clicked category
                        const description = descriptions[index]; // Get category description
                        openModal(category, description); // Show modal
                    }
                }
            }
        })
    } catch (error) {
        console.error("Error fetching pie chart data:", error);
    }
}

async function fetch_student_pie_chart_data() {
    try {
        const response = await fetch("http://localhost:8000/api/student-pie-chart/"); // Call Django API
        const result = await response.json();

        // Extract labels and data
        const labels = result.data.map(item => item.category);  // Extract category names
        const scores = result.data.map(item => item.score);      // Extract corresponding scores
        const descriptions = result.data.map(item => item.description); // Extract descriptions

        // Define chart data
        const data = {
            labels: labels,
            datasets: [{
                data: scores,



                backgroundColor: [
                    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
                    "#9966FF", "#FF9F40", "#FF6384", "#36A2EB",
                    "#FFCE56", "#4BC0C0", "#9966FF"
                ],
                hoverOffset: 40 // Effect when hovering
            }]
        };

        // Render Chart
        const ctx = document.getElementById("student_pie_chart").getContext("2d");
        const student_pie_chart = new Chart(ctx, {
            type: "pie",
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: "bottom" } },
                onClick: function (event, elements) {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const category = labels[index]; // Get clicked category
                        const description = descriptions[index]; // Get category description
                        openModal(category, description); // Show modal
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error fetching pie chart data:", error);
    }
}

function openModal(category, description) {
    document.getElementById("modalTitle").innerText = `Category: ${category}`;
    document.getElementById("modalText").innerText = description;
    document.getElementById("modalOverlay").style.display = "block";
    document.getElementById("infoModal").style.display = "block";
}

function closeModal() {
    document.getElementById("modalOverlay").style.display = "none";
    document.getElementById("infoModal").style.display = "none";
}

// Close button event
document.getElementById("closeBtn").addEventListener("click", closeModal);

// Run function when page loads
fetch_student_pie_chart_data()
fetch_instructor_pie_chart_data()




