# db_utils.py

import sqlite3

from config import DB_PATH

def run_query(query, params=()):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows

    except Exception as e:
        return f"Error in DB: {str(e)}"