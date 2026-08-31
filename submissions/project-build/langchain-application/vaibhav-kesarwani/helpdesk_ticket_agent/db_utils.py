import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
os.environ["DB_PATH"] = os.getenv("DB_PATH")

def get_connection():
    return sqlite3.connect(os.environ["DB_PATH"])


def run_select_query(query, params=()):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    conn.close()

    return [dict(row) for row in rows]


def run_write_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()

    conn.close()