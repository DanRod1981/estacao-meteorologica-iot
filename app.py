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

    </div>

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
