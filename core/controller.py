import time

from core import climate
from core import validator
from core import alarms

from hardware import sensors

from storage import database

from core.state import state


def run():

    while True:

        try:

            # ---------- READ REAL SENSORS ----------
            sensors.refresh_sensors()


            # ---------- CONTROL SYSTEM ----------
            climate.update_controls()


            # ---------- VALIDATION ----------
            validator.validate_sensors()


            # ---------- ALARMS ----------
            alarms.check_alarms()


            # ---------- DATABASE ----------
            database.log_telemetry(
                state.humidity,
                state.co2,
                state.temperature,
                state.fan_on,
                state.mister_on
            )


            print(
                f"H:{state.humidity}% "
                f"CO2:{state.co2}ppm "
                f"T:{state.temperature}C"
            )


            time.sleep(5)


        except Exception as e:

            print("CONTROLLER ERROR:")
            print(e)

            time.sleep(5)