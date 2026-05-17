from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "adminpass"),
    "database": os.getenv("DB_NAME", "weather_db"),
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/data")
def data():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        if row.get("timestamp"):
            row["timestamp"] = str(row["timestamp"])
    return jsonify(rows)


@app.route("/")
def index():
    return """
    <html><body>
    <h2>Агрегатор погоды — г. Сочи</h2>
    <ul>
        <li><a href="/data">Данные JSON</a></li>
        <li><a href="/pgadmin">Администрирование БД</a></li>
        <li><a href="/metabase">Аналитика</a></li>
    </ul>
    </body></html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
