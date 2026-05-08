from flask import Flask, jsonify, render_template
import threading

import controller
import database
import config_manager

from state import state

app = Flask(__name__)


config = config_manager.load_config()

state.target_humidity = config["target_humidity"]
state.target_co2 = config["target_co2"]


database.initialize_database()


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

        "auto_mode": state.auto_mode,

        "target_humidity": state.target_humidity,
        "target_co2": state.target_co2,

        "alarm_active": state.alarm_active,
        "alarm_message": state.alarm_message,

        "sensor_fault": state.sensor_fault,
        "sensor_fault_message": state.sensor_fault_message,
        "fan_runtime": state.total_fan_seconds,
        "mister_runtime": state.total_mister_seconds
    })


@app.route("/api/history")
def history():

    rows = database.get_recent_telemetry()

    history = []

    for row in rows:

        history.append({
            "timestamp": row[0],
            "humidity": row[1],
            "co2": row[2],
            "temperature": row[3],
            "fan_on": bool(row[4]),
            "mister_on": bool(row[5])
        })

    return jsonify(history)


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


@app.route("/set-targets/<humidity>/<co2>")
def set_targets(humidity, co2):

    state.target_humidity = float(humidity)
    state.target_co2 = int(co2)

    config_manager.save_config({
        "target_humidity": state.target_humidity,
        "target_co2": state.target_co2
    })

    return "OK"


if __name__ == "__main__":

    thread = threading.Thread(target=controller.run)

    thread.daemon = True

    thread.start()

    app.run(host="0.0.0.0", port=5000)