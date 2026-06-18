// ===== THEME =====

function applyTheme() {
    const saved = localStorage.getItem("theme");

    if (saved === "light") {
        document.body.classList.add("light");

        const btn = document.querySelector(".theme-btn");

        if(btn){
            btn.innerText = "☀️";
        }

    } else {

        document.body.classList.remove("light");

        const btn = document.querySelector(".theme-btn");

        if(btn){
            btn.innerText = "🌙";
        }
    }
}

function toggleTheme() {

    const body = document.body;

    if (body.classList.contains("light")) {

        body.classList.remove("light");
        localStorage.setItem("theme", "dark");

    } else {

        body.classList.add("light");
        localStorage.setItem("theme", "light");
    }

    applyTheme();
}

// ===== DELETE =====

function confirmDelete() {
    return confirm("Are you sure you want to delete this job?");
}

// ===== PAGE LOAD =====

window.addEventListener("DOMContentLoaded", () => {

    applyTheme();

    const chartDataElement = document.getElementById("chart-data");

    if (!chartDataElement) return;

    const DATA = JSON.parse(chartDataElement.textContent);

    // STATUS CHART

    const statusCanvas = document.getElementById("statusChart");

    if (statusCanvas) {

        new Chart(statusCanvas, {
            type: "doughnut",

            data: {
                labels: ["Applied", "Interview", "Rejected"],

                datasets: [{
                    data: DATA.status,
                    backgroundColor: [
                        "#facc15",
                        "#38bdf8",
                        "#ef4444"
                    ]
                }]
            }
        });
    }

    // TREND CHART

    const trendCanvas = document.getElementById("trendChart");

    if (trendCanvas) {

        new Chart(trendCanvas, {
            type: "line",

            data: {
                labels: DATA.months,

                datasets: [{
                    label: "Applications",
                    data: DATA.trend,
                    borderColor: "#38bdf8",
                    fill: true
                }]
            }
        });
    }

});

// ===== DRAG & DROP =====

const jobs = document.querySelectorAll(".job");
const columns = document.querySelectorAll(".kanban-column");

let draggedJob = null;

// DRAG START
jobs.forEach(job => {

    job.addEventListener("dragstart", () => {

        draggedJob = job;

        job.classList.add("dragging");

    });

    job.addEventListener("dragend", () => {

        job.classList.remove("dragging");

    });

});

// COLUMN EVENTS
columns.forEach(column => {

   column.addEventListener("dragover", (e) => {

    e.preventDefault();

    column.classList.add("drag-over");

});
    
column.addEventListener("dragleave", () => {

    column.classList.remove("drag-over");

});

    column.addEventListener("drop", () => {

        column.classList.remove("drag-over");
        if(draggedJob){

            column.appendChild(draggedJob);

            const jobId = draggedJob.dataset.id;

            const newStatus = column.id;

            // UPDATE STATUS BADGE LIVE
const badge = draggedJob.querySelector("[data-status]");

if(badge){

    badge.textContent = newStatus;

    badge.className = `tag ${newStatus}`;

}

            // UPDATE DATABASE
            fetch(`/drag-update/${jobId}`, {

                method:"POST",

                headers:{
                    "Content-Type":"application/x-www-form-urlencoded"
                },

                body:`status=${newStatus}`

            });
           updateEmptyColumns(); 

        }

    });

});
// ===== EMPTY COLUMN HANDLER =====

function updateEmptyColumns(){

    document.querySelectorAll(".kanban-column").forEach(column => {

        const jobs = column.querySelectorAll(".job");

        const empty = column.querySelector(".empty-column");

        if(jobs.length > 0){

            empty.style.display = "none";

        } else {

            empty.style.display = "block";

        }

    });

    document.querySelectorAll(".kanban-column").forEach(column => {

    const jobs = column.querySelectorAll(".job");
    const empty = column.querySelector(".empty-column");

    if(jobs.length > 0){
        empty.style.display = "none";
    }

});

}

// RUN ON LOAD
updateEmptyColumns();

// LIVE SEARCH

const searchInput = document.getElementById("liveSearch");

if(searchInput){

    searchInput.addEventListener("keyup", function(){

        const value = this.value.toLowerCase();

        document.querySelectorAll(".job").forEach(job => {

            const text = job.innerText.toLowerCase();

            if(text.includes(value)){
                job.style.display = "flex";
            }
            else{
                job.style.display = "none";
            }

        });

    });

}

setTimeout(() => {

    const flash =
        document.querySelector(".flash-message");

    if(flash){
        flash.style.display = "none";
    }

}, 3000);

function toggleSidebar() {
    document.querySelector(".sidebar").classList.toggle("show");
}

function toggleSection(id){
    document.getElementById(id).classList.toggle("show");
}
