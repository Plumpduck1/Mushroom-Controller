import csv
import os
from datetime import datetime

FILE_NAME = "data/log.csv"


def log_data(humidity, co2, temperature, fan_on, mister_on):

    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "humidity",
                "co2",
                "temperature",
                "fan_on",
                "mister_on"
            ])

        writer.writerow([
            datetime.now(),
            humidity,
            co2,
            temperature,
            fan_on,
            mister_on
        ])