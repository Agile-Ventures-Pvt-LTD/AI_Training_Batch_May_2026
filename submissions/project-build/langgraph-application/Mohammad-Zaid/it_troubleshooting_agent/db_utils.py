import sqlite3
from config import DB_PATH


def db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def run_query(query: str, params: tuple = ()):
    conn = db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else "No records found."
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        conn.close()
