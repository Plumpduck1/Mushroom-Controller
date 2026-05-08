from state import state


def update_environment():

    if state.mister_on:
        state.humidity += 0.5
    else:
        state.humidity -= 0.2

    if state.fan_on:
        state.co2 -= 50
        state.humidity -= 0.3
    else:
        state.co2 += 50

    state.humidity = max(70, min(100, state.humidity))
    state.co2 = max(400, min(2000, state.co2))
