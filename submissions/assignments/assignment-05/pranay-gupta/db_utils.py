import sqlite3
import json
from config import DB_PATH


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def execute_select_query(query: str, params: tuple = ()):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]

        if not result:
            return "No records found."

        return json.dumps(result, indent=2)

    except Exception as e:
        return f"Database Error: {str(e)}"

    finally:
        conn.close()