const labels = JSON.parse(document.getElementById("chartData").dataset.labels);
const valores = JSON.parse(document.getElementById("chartData").dataset.valores);
const ctx = document.getElementById("graficoReservas").getContext("2d");
new Chart(ctx, {
    type: "line",
    data: {
        labels: labels,
        datasets: [{
            label: "Reservas",
            data: valores,
            borderColor: "#2d6a4f",
            backgroundColor: "rgba(45, 106, 79, 0.1)",
            borderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: ctx => `reservas : ${ctx.parsed.y}`
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: { color: "rgba(0,0,0,0.05)" }
            },
            x: {
                grid: { display: false }
            }
        },
        interaction: {
            mode: 'index',
            intersect: false
        }
    }
});