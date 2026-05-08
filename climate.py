import simulation


def update_controls():

    if not simulation.auto_mode:
        return

    if simulation.humidity < 90:
        simulation.mister_on = True
    elif simulation.humidity > 95:
        simulation.mister_on = False

    if simulation.co2 > 1200:
        simulation.fan_on = True
    elif simulation.co2 < 700:
        simulation.fan_on = False