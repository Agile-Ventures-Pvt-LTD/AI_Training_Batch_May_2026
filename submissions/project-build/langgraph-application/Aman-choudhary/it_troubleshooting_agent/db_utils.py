import sqlite3
from config import DB_PATH
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def fetch_all(query,params=()):
    conn = get_connection()
    rows = conn.execute(query,params).fetchall()
    conn.close()
    return [dict(row)for row in rows]
def fetch_one(query,params=()):
    conn = get_connection()
    row = conn.execute(query,params).fetchone()
    conn.close()
    if row:
        return dict(row)
    return {}