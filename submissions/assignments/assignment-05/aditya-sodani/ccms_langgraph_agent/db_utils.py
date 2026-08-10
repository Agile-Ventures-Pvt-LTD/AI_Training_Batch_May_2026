import sqlite3
import os
from config import config
DB_PATH = config.DB_PATH
def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found:{DB_PATH}")   
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def execute_query(query: str, params: tuple = ()) -> list[dict]:
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)

        rows = [dict(row) for row in cursor.fetchall()]
        return rows

    except Exception as e:
        raise e

    finally:
        if conn:
            conn.close()
def execute_fetchone(query: str, params: tuple = ()) -> dict | None:
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()