import sqlite3
import os

DB_NAME = "vehicles.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS owners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate TEXT NOT NULL UNIQUE,
        brand TEXT,
        model TEXT,
        year INTEGER,
        owner_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES owners (id)
    );
    """)

    conn.commit()
    conn.close()

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO owners (id, name, phone, email) VALUES (1, 'Juan Pérez', '6671234567', 'juan@example.com')")
    cursor.execute("INSERT OR IGNORE INTO vehicles (plate, brand, model, year, owner_id) VALUES ('VBA1234', 'Nissan', 'Versa', 2020, 1)")

    cursor.execute("INSERT OR IGNORE INTO owners (id, name, phone, email) VALUES (2, 'María López', '6679876543', 'maria@example.com')")
    cursor.execute("INSERT OR IGNORE INTO vehicles (plate, brand, model, year, owner_id) VALUES ('ABC9876', 'Toyota', 'Corolla', 2018, 2)")

    conn.commit()
    conn.close()

if not os.path.exists(DB_NAME):
    init_db()
    seed_data()
