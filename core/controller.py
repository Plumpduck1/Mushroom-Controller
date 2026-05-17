import time

from core.state import state

from hardware import sensors
from hardware import fan


# ============================================
# TARGETS
# ============================================

TARGET_HUMIDITY = 90
MAX_HUMIDITY = 96

TARGET_CO2 = 1200
MAX_CO2 = 2500


# ============================================
# SCALE FUNCTION
# ============================================

def scale(
    value,
    min_input,
    max_input,
    min_output,
    max_output
):

    if value <= min_input:

        return min_output

    if value >= max_input:

        return max_output

    normalized = (
        value - min_input
    ) / (
        max_input - min_input
    )

    return (
        min_output +
        normalized * (
            max_output - min_output
        )
    )


# ============================================
# MAIN CONTROLLER
# ============================================

def run_controller():

    while True:

        # ============================================
        # MANUAL MODE LOCKOUT
        # ============================================

        if not state.auto_mode:

            print(
                "Manual mode active"
            )

            time.sleep(1)

            continue


        try:

            # ============================================
            # SENSOR REFRESH
            # ============================================

            sensors.refresh_sensors()


            humidity = state.humidity
            co2 = state.co2


            fan_speed = 0
            reason = "Idle"


            # ============================================
            # CO2 CONTROL
            # ============================================

            if co2 is not None:

                if co2 > TARGET_CO2:

                    fan_speed = scale(
                        co2,
                        TARGET_CO2,
                        MAX_CO2,
                        0.3,
                        1.0
                    )

                    reason = (
                        f"High CO2 ({co2} ppm)"
                    )


            # ============================================
            # HUMIDITY CONTROL
            # ============================================

            if humidity is not None:

                if humidity > TARGET_HUMIDITY:

                    humidity_speed = scale(
                        humidity,
                        TARGET_HUMIDITY,
                        MAX_HUMIDITY,
                        0.2,
                        0.8
                    )

                    if humidity_speed > fan_speed:

                        fan_speed = humidity_speed

                        reason = (
                            f"High humidity ({humidity}%)"
                        )


            # ============================================
            # APPLY FAN SPEED
            # ============================================

            fan.set_speed(
                fan_speed
            )


            # ============================================
            # SAVE STATE
            # ============================================

            state.fan_speed = round(
                fan_speed * 100,
                1
            )

            state.fan_reason = reason

            state.fan_on = (
                fan_speed > 0
            )


            # ============================================
            # DEBUG
            # ============================================

            print(

                f"H:{humidity}% "

                f"CO2:{co2}ppm "

                f"Fan:{state.fan_speed}% "

                f"Reason:{reason}"

            )


        except Exception as e:

            print(
                "CONTROLLER ERROR:"
            )

            print(e)


        time.sleep(5)