import sqlite3
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def execute_query(query, params=()):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute(query, params)

    rows = cur.fetchall()

    conn.close()

    return [dict(r) for r in rows]