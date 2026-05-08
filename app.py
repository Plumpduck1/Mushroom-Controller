from flask import Flask, jsonify, render_template
import csv
import threading
import controller

from state import state

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/data")
def data():

    return jsonify({
        "humidity": round(state.humidity, 1),
        "co2": state.co2,
        "temperature": state.temperature,
        "fan_on": state.fan_on,
        "mister_on": state.mister_on,
        "auto_mode": state.auto_mode
    })


@app.route("/api/history")
def history():

    rows = []

    with open("data/log.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    rows = rows[-50:]

    return jsonify(rows)


@app.route("/toggle-auto")
def toggle_auto():

    state.auto_mode = not state.auto_mode

    return "OK"


@app.route("/fan/on")
def fan_on():

    state.fan_on = True
    return "OK"


@app.route("/fan/off")
def fan_off():

    state.fan_on = False
    return "OK"


@app.route("/mister/on")
def mister_on():

    state.mister_on = True
    return "OK"


@app.route("/mister/off")
def mister_off():

    state.mister_on = False
    return "OK"


if __name__ == "__main__":

    thread = threading.Thread(target=controller.run)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=5000)