from gpiozero import PWMOutputDevice


# ============================================
# FAN PWM MOSFET
#
# GPIO13 = physical pin 33
# ============================================

fan = PWMOutputDevice(
    13,
    frequency=5000
)


current_speed = 0


# ============================================
# SET FAN SPEED
# ============================================

def set_speed(speed):

    global current_speed

    speed = max(
        0,
        min(1, speed)
    )

    fan.value = speed

    current_speed = speed


# ============================================
# GET FAN SPEED
# ============================================

def get_speed():

    return current_speed