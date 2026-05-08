import time
import simulation
import climate
import logger
from state import state


def run():

    while True:

        climate.update_controls()
        simulation.update_environment()

        logger.log_data(
            state.humidity,
            state.co2,
            state.temperature,
            state.fan_on,
            state.mister_on
        )

        time.sleep(1)