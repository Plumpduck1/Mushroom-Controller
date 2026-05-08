from state import state
import sensors
import actuators


def update_controls():

    if state.sensor_fault:
        return

    if not state.auto_mode:
        return

    humidity = sensors.read_humidity()
    co2 = sensors.read_co2()

    if humidity < state.target_humidity:
        actuators.set_mister(True)

    elif humidity > state.target_humidity + 3:
        actuators.set_mister(False)

    if co2 > state.target_co2:
        actuators.set_fan(True)

    elif co2 < state.target_co2 - 200:
        actuators.set_fan(False)