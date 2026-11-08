const ctx = document.getElementById('graficoTemperatura');

const grafico = new Chart(ctx, {
    type: 'line',
    data: {
        labels: temperaturas.map((_, i) => i + 1),
        datasets: [
        {
            label: 'Temperatura °C',
            data: temperaturas,
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56,189,248,0.2)',
            borderWidth: 2,
            tension: 0.3
        },
        {
            label: 'Umidade %',
            data: umidades,
            borderColor: '#22c55e',
            backgroundColor: 'rgba(34,197,94,0.2)',
            borderWidth: 2,
            tension: 0.3
        }
        ]
    },
    options: {
        responsive: true
    }
});

async function atualizarGrafico() {

    const resposta = await fetch('/api/dados');

    const dados = await resposta.json();
    document.getElementById('temperaturaAtual').innerText =
    dados.temperatura + " °C";

    document.getElementById('umidadeAtual').innerText =
    dados.umidade + " %";

    grafico.data.labels =
        dados.temperaturas.map((_, i) => i + 1);

    grafico.data.datasets[0].data =
        dados.temperaturas;

    grafico.data.datasets[1].data =
        dados.umidades;

    grafico.update();
}

setInterval(atualizarGrafico, 5000);