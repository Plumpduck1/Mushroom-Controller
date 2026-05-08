from state import state


def check_alarms():
    
    if state.sensor_fault:
        return

    state.alarm_active = False
    state.alarm_message = ""

    if state.humidity > 98:
        state.alarm_active = True
        state.alarm_message = "Humidity dangerously high"

    elif state.co2 > 5000:
        state.alarm_active = True
        state.alarm_message = "CO2 dangerously high"

    elif state.temperature > 30:
        state.alarm_active = True
        state.alarm_message = "Temperature dangerously high"