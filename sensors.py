from state import state


def read_humidity():
    return state.humidity


def read_co2():
    return state.co2


def read_temperature():
    return state.temperature