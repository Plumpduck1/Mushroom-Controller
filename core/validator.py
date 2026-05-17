from core.state import state


def validate_sensors():

    state.sensor_fault = False
    state.sensor_fault_message = ""

    if state.humidity is None:
        state.sensor_fault = True
        state.sensor_fault_message = "Humidity sensor disconnected"

    elif state.humidity < 20 or state.humidity > 100:
        state.sensor_fault = True
        state.sensor_fault_message = "Humidity sensor reading invalid"

    elif state.co2 < 300 or state.co2 > 10000:
        state.sensor_fault = True
        state.sensor_fault_message = "CO2 sensor reading invalid"

    elif state.temperature < 5 or state.temperature > 40:
        state.sensor_fault = True
        state.sensor_fault_message = "Temperature sensor reading invalid"