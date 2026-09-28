from flask import Flask, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

temperatura = 0
umidade = 0

db = sqlite3.connect("clima.db", check_same_thread=False)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leituras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura REAL,
    umidade REAL,
    datahora TEXT
)
""")

db.commit()

@app.route("/")
def home():

    cursor.execute("""
    SELECT temperatura, umidade, datahora
    FROM leituras
    ORDER BY id DESC
    LIMIT 5
    """)

    leituras = cursor.fetchall()
    
    temperaturas = []

    for temp, umi, datahora in reversed(leituras):
        temperaturas.append(temp)

    dados_grafico = str(temperaturas)

    historico = ""

    for temp, umi, datahora in leituras:

        historico += f"""
        <tr>
            <td>{temp} °C</td>
            <td>{umi} %</td>
            <td>{datahora}</td>
        </tr>
        """

    return f"""

<html>
<head>

<title>Estação Meteorológica IoT</title>

<style>

body {{
background: #1e293b;
color: white;
font-family: Arial, sans-serif;
text-align: center;
margin-top: 50px;
}}

.card {{
background: #334155;
width: 500px;
margin: auto;
padding: 30px;
border-radius: 20px;
box-shadow: 0 0 20px rgba(0,0,0,0.4);
}}

.valor {{
font-size: 50px;
font-weight: bold;
}}

.titulo {{
font-size: 20px;
color: #cbd5e1;
}}

</style>

</head>

<body>

<div class="card">

<h1>🌤 Estação Meteorológica IoT</h1>

<br>

<div class="titulo">
🌡 Temperatura
</div>

<div class="valor">
{temperatura} °C
</div>

<br>

<div class="titulo">
💧 Umidade
</div>

<div class="valor">
{umidade} %
</div>

<br><br>

<p>✅ ESP32 Online</p>

<hr>

<h3>📜 Últimas Leituras</h3>

<h3>📈 Gráfico de Temperatura</h3>

<canvas id="graficoTemperatura"></canvas>

<table style="width:100%; color:white;">

<tr>
<th>Temperatura</th>
<th>Umidade</th>
<th>Data/Hora</th>
</tr>

{historico}

</table>


</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>

const temperaturas = {dados_grafico};

document.write("");

console.log(temperaturas);

</script>

</body>

</html>
"""


@app.route("/dados")
def dados():

    global temperatura
    global umidade

    temperatura = request.args.get("temp")
    umidade = request.args.get("umi")

    cursor.execute("""
	INSERT INTO leituras
	(temperatura, umidade, datahora)
	VALUES (?, ?, ?)

	""", (

	float(temperatura),
	float(umidade),

	datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    db.commit()

    return "OK"


app.run(host="0.0.0.0", port=5000)
