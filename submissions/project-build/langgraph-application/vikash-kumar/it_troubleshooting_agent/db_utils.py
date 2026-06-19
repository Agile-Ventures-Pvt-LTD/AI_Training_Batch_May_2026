import sqlite3
from config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_select_query(query: str,params: tuple = ()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query,params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

