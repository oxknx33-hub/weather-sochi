import requests
import mysql.connector
import time
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "adminpass"),
    "database": os.getenv("DB_NAME", "weather_db"),
}

CITY = "Sochi"
LAT = 43.6
LON = 39.73


def get_db():
    for i in range(15):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            print("DB connected")
            return conn
        except Exception as e:
            print(f"Waiting for DB ({i+1}/15): {e}")
            time.sleep(4)
    raise RuntimeError("Cannot connect to DB")


def fetch_open_meteo():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current": "temperature_2m,wind_speed_10m,wind_direction_10m",
        "wind_speed_unit": "ms",
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    c = r.json()["current"]
    return {
        "source": "open-meteo",
        "city": CITY,
        "value": c["temperature_2m"],
        "unit": "celsius",
        "wind_speed": c["wind_speed_10m"],
        "wind_direction": str(c["wind_direction_10m"]),
    }


def fetch_gismeteo_mock():
    import random
    return {
        "source": "gismeteo",
        "city": CITY,
        "value": round(random.uniform(18.0, 28.0), 1),
        "unit": "celsius",
        "wind_speed": round(random.uniform(1.0, 8.0), 1),
        "wind_direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]),
    }


def save(conn, record):
    cursor = conn.cursor()
    sql = """INSERT INTO weather_data
             (source, city, value, unit, wind_speed, wind_direction)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (
        record["source"], record["city"], record["value"],
        record["unit"], record["wind_speed"], record["wind_direction"],
    ))
    conn.commit()
    cursor.close()
    print(f"Saved: {record['source']} | {record['value']}°C")


if __name__ == "__main__":
    conn = get_db()
    while True:
        try:
            save(conn, fetch_open_meteo())
            save(conn, fetch_gismeteo_mock())
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(600)
