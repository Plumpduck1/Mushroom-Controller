from state import state


def update_controls():

    if not state.auto_mode:
        return

    if state.humidity < 90:
        state.mister_on = True
    elif state.humidity > 95:
        state.mister_on = False

    if state.co2 > 1200:
        state.fan_on = True
    elif state.co2 < 700:
        state.fan_on = False