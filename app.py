from flask import Flask, request, render_template
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
    umidades = []

    for temp, umi, datahora in reversed(leituras):
        temperaturas.append(temp)
        umidades.append(umi)

    dados_grafico = str(temperaturas)
    dados_umidade = str(umidades)

    historico = ""

    for temp, umi, datahora in leituras:

        historico += f"""
        <tr>
            <td>{temp} °C</td>
            <td>{umi} %</td>
            <td>{datahora}</td>
        </tr>
        """

    return render_template(
    "index.html",
    temperatura=temperatura,
    umidade=umidade,
    historico=historico,
    dados_grafico=dados_grafico,
    dados_umidade=dados_umidade
    )

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
