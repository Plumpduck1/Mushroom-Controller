from core.state import state


def set_fan(on):

    state.fan_on = on

    # Future:
    # GPIO.output(FAN_PIN, GPIO.HIGH)


def set_mister(on):

    state.mister_on = on

    # Future:
    # GPIO.output(MISTER_PIN, GPIO.HIGH)


def set_light(on):

    state.light_on = on

    # Future:
    # GPIO.output(LIGHT_PIN, GPIO.HIGH)