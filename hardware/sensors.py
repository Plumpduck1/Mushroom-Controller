from core.state import state


def read_humidity():

    return state.humidity


def read_co2():

    return state.co2


def read_temperature():

    return state.temperature


def refresh_sensors():
    """
    Placeholder for future real sensor updates.

    Later this will:
    - read BME280
    - read SCD41
    - update state values
    """

    pass