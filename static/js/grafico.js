const ctx = document.getElementById('graficoTemperatura');

new Chart(ctx, {
    type: 'line',
    data: {
        labels: temperaturas.map((_, i) => i + 1),
        datasets: [{
            label: 'Temperatura °C',
            data: temperaturas,
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56,189,248,0.2)',
            borderWidth: 2,
            tension: 0.3
        }]
    },
    options: {
        responsive: true
    }
});