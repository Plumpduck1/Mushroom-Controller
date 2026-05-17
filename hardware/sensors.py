from smbus2 import SMBus

import time
import board
import busio

from adafruit_bme280 import basic as adafruit_bme280

from core.state import state


# ============================================
# BME280
# ============================================

bme280 = None

for attempt in range(5):

    try:

        i2c = busio.I2C(
            board.SCL,
            board.SDA
        )

        bme280 = (
            adafruit_bme280.Adafruit_BME280_I2C(
                i2c,
                address=0x76
            )
        )

        print(
            "BME280 initialized"
        )

        break

    except Exception as e:

        print(
            f"BME280 init retry "
            f"{attempt + 1} failed:",
            e
        )

        time.sleep(1)


# ============================================
# SCD41
# ============================================

ADDR = 0x62

bus = SMBus(1)

last_co2_read_time = 0

cached_co2 = None
cached_scd_temp = None
cached_scd_humidity = None


# ============================================
# START SCD41
# ============================================

print(
    "Waiting for SCD41 startup..."
)

# IMPORTANT:
# SCD41 needs startup time

time.sleep(5)


started = False

for attempt in range(5):

    try:

        bus.write_i2c_block_data(
            ADDR,
            0x21,
            [0xB1]
        )

        print(
            "SCD41 measurement started"
        )

        time.sleep(5)

        started = True

        break

    except Exception as e:

        print(
            f"SCD41 startup retry "
            f"{attempt + 1} failed:",
            e
        )

        time.sleep(2)


if not started:

    print(
    "SCD41 start command failed "
    "but sensor may already "
    "be measuring"
)


# ============================================
# READ SCD41
# ============================================

def read_scd41():

    global last_co2_read_time
    global cached_co2
    global cached_scd_temp
    global cached_scd_humidity

    current_time = time.time()


    # ============================================
    # CACHE
    # ============================================

    if (

        cached_co2 is not None

        and

        current_time -
        last_co2_read_time < 10

    ):

        return (

            cached_co2,

            cached_scd_temp,

            cached_scd_humidity

        )


    # ============================================
    # RETRIES
    # ============================================

    for attempt in range(3):

        try:

            # READ MEASUREMENT COMMAND

            bus.write_i2c_block_data(
                ADDR,
                0xEC,
                [0x05]
            )

            time.sleep(0.05)


            # READ RESPONSE

            data = bus.read_i2c_block_data(
                ADDR,
                0x00,
                9
            )


            # CO2

            co2 = (

                (data[0] << 8)

                | data[1]

            )


            # TEMPERATURE

            temp_raw = (

                (data[3] << 8)

                | data[4]

            )

            temperature = (

                -45 +

                175 * (
                    temp_raw / 65535.0
                )

            )


            # HUMIDITY

            hum_raw = (

                (data[6] << 8)

                | data[7]

            )

            humidity = (

                100 * (
                    hum_raw / 65535.0
                )

            )


            # SAVE CACHE

            cached_co2 = co2

            cached_scd_temp = (
                temperature
            )

            cached_scd_humidity = (
                humidity
            )

            last_co2_read_time = (
                current_time
            )


            return (

                co2,

                temperature,

                humidity

            )


        except Exception as e:

            print(
                f"SCD41 retry "
                f"{attempt + 1} failed:",
                e
            )

            time.sleep(0.2)


    print(
        "SCD41 failed after retries"
    )

    return (
        None,
        None,
        None
    )


# ============================================
# BME280 HELPERS
# ============================================

def read_temperature():

    if bme280 is None:

        return None

    try:

        return round(
            bme280.temperature,
            2
        )

    except Exception as e:

        print(
            "Temperature read error:",
            e
        )

        return None


def read_humidity():

    if bme280 is None:

        return None

    try:

        return round(
            bme280.relative_humidity,
            2
        )

    except Exception as e:

        print(
            "Humidity read error:",
            e
        )

        return None


def read_pressure():

    if bme280 is None:

        return None

    try:

        return round(
            bme280.pressure,
            2
        )

    except Exception as e:

        print(
            "Pressure read error:",
            e
        )

        return None


# ============================================
# LEGACY CO2
# ============================================

def read_co2():

    return state.co2


# ============================================
# MAIN REFRESH
# ============================================

def refresh_sensors():

    try:

        # ============================================
        # SCD41
        # ============================================

        co2 = None
        scd_temp = None
        scd_humidity = None

        try:

            co2, scd_temp, scd_humidity = (
                read_scd41()
            )

        except Exception as e:

            print(
                "SCD41 unavailable:",
                e
            )


        # ============================================
        # BME280
        # ============================================

        bme_temp = (
            read_temperature()
        )

        bme_humidity = (
            read_humidity()
        )

        bme_pressure = (
            read_pressure()
        )


        # ============================================
        # TEMPERATURE BLEND
        # ============================================

        if (

            bme_temp is not None

            and

            scd_temp is not None

        ):

            state.temperature = round(

                (bme_temp * 0.7)

                +

                (scd_temp * 0.3),

                2

            )

        elif bme_temp is not None:

            state.temperature = (
                bme_temp
            )

        elif scd_temp is not None:

            state.temperature = round(
                scd_temp,
                2
            )

        else:

            state.temperature = None


        # ============================================
        # HUMIDITY BLEND
        # ============================================

        if (

            bme_humidity is not None

            and

            scd_humidity is not None

        ):

            state.humidity = round(

                (bme_humidity * 0.7)

                +

                (scd_humidity * 0.3),

                2

            )

        elif bme_humidity is not None:

            state.humidity = (
                bme_humidity
            )

        elif scd_humidity is not None:

            state.humidity = round(
                scd_humidity,
                2
            )

        else:

            state.humidity = None


        # ============================================
        # CO2
        # ============================================

        state.co2 = co2


        # ============================================
        # PRESSURE
        # ============================================

        state.pressure = (
            bme_pressure
        )


        # ============================================
        # SENSOR STATUS
        # ============================================

        state.sensor_fault = False

        state.sensor_fault_message = ""


        if (
            state.co2 is None
            and
            bme_temp is not None
        ):

            state.sensor_fault = True

            state.sensor_fault_message = (
                "CO2 sensor offline"
            )


        elif (
            bme_temp is None
            and
            state.co2 is not None
        ):

            state.sensor_fault = True

            state.sensor_fault_message = (
                "BME280 sensor offline"
            )


        elif (
            bme_temp is None
            and
            state.co2 is None
        ):

            state.sensor_fault = True

            state.sensor_fault_message = (
                "All sensors offline"
            )


    except Exception as e:

        print(
            "Sensor refresh error:",
            e
        )