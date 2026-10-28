import sqlite3

DB_PATH = "./db/travel_data.db"

def get_connection():
    try:
        return sqlite3.connect(DB_PATH)
    except Exception as e:
        return f"Error Connecting to Database {e}"