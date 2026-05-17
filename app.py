from flask import Flask
from flask import jsonify
from flask import render_template

import threading

from core import controller
from core.state import state

from storage import database
from storage import config_manager

from hardware import fan


# ============================================
# FLASK APP
# ============================================

app = Flask(__name__)


# ============================================
# LOAD CONFIG
# ============================================

config = config_manager.load_config()

state.target_humidity = (
    config["target_humidity"]
)

state.target_co2 = (
    config["target_co2"]
)


# ============================================
# INIT DATABASE
# ============================================

database.initialize_database()


# ============================================
# DASHBOARD
# ============================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================
# LIVE API DATA
# ============================================

@app.route("/api/data")
def data():

    return jsonify({


        # ============================================
        # SENSOR DATA
        # ============================================

        "humidity": (

            round(state.humidity, 1)

            if state.humidity is not None

            else None
        ),


        "co2": (

            round(state.co2, 1)

            if state.co2 is not None

            else None
        ),


        "temperature": (

            round(state.temperature, 1)

            if state.temperature is not None

            else None
        ),


        "pressure": (

            round(state.pressure, 1)

            if state.pressure is not None

            else None
        ),


        # ============================================
        # DEVICE STATES
        # ============================================

        "fan_on":
            state.fan_on,

        "mister_on":
            state.mister_on,

        "auto_mode":
            state.auto_mode,


        # ============================================
        # TARGETS
        # ============================================

        "target_humidity":
            state.target_humidity,

        "target_co2":
            state.target_co2,


        # ============================================
        # ALARMS
        # ============================================

        "alarm_active":
            state.alarm_active,

        "alarm_message":
            state.alarm_message,


        # ============================================
        # SENSOR FAULTS
        # ============================================

        "sensor_fault":
            state.sensor_fault,

        "sensor_fault_message":
            state.sensor_fault_message,


        # ============================================
        # FAN CONTROLLER
        # ============================================

        "fan_speed":

            getattr(
                state,
                "fan_speed",
                0
            ),


        "fan_reason":

            getattr(
                state,
                "fan_reason",
                "Idle"
            ),


        "fan_rpm":

            getattr(
                state,
                "fan_rpm",
                0
            ),


        # ============================================
        # RUNTIME TRACKING
        # ============================================

        "fan_runtime":
            state.total_fan_seconds,

        "mister_runtime":
            state.total_mister_seconds

    })


# ============================================
# HISTORY API
# ============================================

@app.route("/api/history")
def history():

    rows = database.get_recent_telemetry()

    history = []

    for row in rows:

        history.append({

            "timestamp":
                row[0],

            "humidity":
                row[1],

            "co2":
                row[2],

            "temperature":
                row[3],

            "fan_on":
                bool(row[4]),

            "mister_on":
                bool(row[5])

        })

    return jsonify(history)


# ============================================
# TOGGLE AUTO MODE
# ============================================

@app.route("/toggle-auto")
def toggle_auto():

    state.auto_mode = (
        not state.auto_mode
    )

    return "OK"


# ============================================
# FAN CONTROL
# ============================================

@app.route("/fan/on")
def fan_on():

    fan.set_speed(1)

    state.auto_mode = False

    state.fan_on = True

    state.fan_speed = 100

    state.fan_reason = (
        "Manual ON"
    )

    return "OK"


@app.route("/fan/off")
def fan_off():

    fan.set_speed(0)

    state.auto_mode = False

    state.fan_on = False

    state.fan_speed = 0

    state.fan_reason = (
        "Manual OFF"
    )

    return "OK"


# ============================================
# MANUAL PWM CONTROL
# ============================================

@app.route("/fan/pwm/<int:pwm>")
def fan_pwm(pwm):

    pwm = max(
        0,
        min(100, pwm)
    )

    speed = pwm / 100

    fan.set_speed(speed)

    state.auto_mode = False

    state.fan_speed = pwm

    state.fan_reason = (
        "Manual Override"
    )

    state.fan_on = (
        pwm > 0
    )

    return "OK"

# ============================================
# TARGET SETTINGS
# ============================================

@app.route(
    "/set-targets/<humidity>/<co2>"
)
def set_targets(
    humidity,
    co2
):

    state.target_humidity = (
        float(humidity)
    )

    state.target_co2 = (
        int(co2)
    )

    config_manager.save_config({

        "target_humidity":
            state.target_humidity,

        "target_co2":
            state.target_co2

    })

    return "OK"


# ============================================
# START CONTROLLER
# ============================================

if __name__ == "__main__":

    thread = threading.Thread(

        target=controller.run_controller

    )

    thread.daemon = True

    thread.start()

    app.run(

        host="0.0.0.0",
        port=5000

    )