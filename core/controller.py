import time

from core import climate
from core import validator
from core import alarms

from hardware import simulation

from storage import database

from core.state import state


def run():

    while True:

        try:

            climate.update_controls()

            simulation.update_environment()

            validator.validate_sensors()

            alarms.check_alarms()

            database.log_telemetry(
                state.humidity,
                state.co2,
                state.temperature,
                state.fan_on,
                state.mister_on
            )

            print("controller tick")

            time.sleep(1)

        except Exception as e:

            print("CONTROLLER ERROR:")
            print(e)

            time.sleep(1)