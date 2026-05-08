import time
import simulation
import climate
import alarms
import validator
import database

from state import state


def run():

    while True:

        climate.update_controls()

        simulation.update_environment()

        validator.validate_sensors()

        alarms.check_alarms()

        if state.fan_on:
            state.total_fan_seconds += 1

        if state.mister_on:
            state.total_mister_seconds += 1

        database.log_telemetry(
            state.humidity,
            state.co2,
            state.temperature,
            state.fan_on,
            state.mister_on
        )

        time.sleep(1)