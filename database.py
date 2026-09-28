import sqlite3


DATABASE = "plant_history.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant TEXT,
            result TEXT,
            confidence REAL,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()


def save_scan(plant, result, confidence):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO scans (plant, result, confidence)
        VALUES (?, ?, ?)
    """, (plant, result, confidence))

    connection.commit()

    connection.close()


def get_scans():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, plant, result, confidence, date_time
        FROM scans
        ORDER BY id DESC
    """)

    scans = cursor.fetchall()

    connection.close()

    return scans