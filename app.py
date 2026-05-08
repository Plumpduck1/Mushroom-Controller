from flask import Flask, jsonify, render_template
import simulation
import climate

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/data")
def data():

    climate.update_controls()
    simulation.update_environment()

    return jsonify({
        "humidity": round(simulation.humidity, 1),
        "co2": simulation.co2,
        "temperature": simulation.temperature,
        "fan_on": simulation.fan_on,
        "mister_on": simulation.mister_on,
        "auto_mode": simulation.auto_mode
    })


@app.route("/toggle-auto")
def toggle_auto():

    simulation.auto_mode = not simulation.auto_mode

    return "OK"


@app.route("/fan/on")
def fan_on():

    simulation.fan_on = True
    return "OK"


@app.route("/fan/off")
def fan_off():

    simulation.fan_on = False
    return "OK"


@app.route("/mister/on")
def mister_on():

    simulation.mister_on = True
    return "OK"


@app.route("/mister/off")
def mister_off():

    simulation.mister_on = False
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)