import sqlite3
from datetime import datetime

DATABASE_NAME = "data/mushroom.db"


def initialize_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            humidity REAL,
            co2 INTEGER,
            temperature REAL,
            fan_on INTEGER,
            mister_on INTEGER
        )
    """)

    connection.commit()
    connection.close()


def log_telemetry(
    humidity,
    co2,
    temperature,
    fan_on,
    mister_on
):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO telemetry (
            timestamp,
            humidity,
            co2,
            temperature,
            fan_on,
            mister_on
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        humidity,
        co2,
        temperature,
        int(fan_on),
        int(mister_on)
    ))

    connection.commit()
    connection.close()


def get_recent_telemetry(limit=50):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            humidity,
            co2,
            temperature,
            fan_on,
            mister_on
        FROM telemetry
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    rows.reverse()

    return rows