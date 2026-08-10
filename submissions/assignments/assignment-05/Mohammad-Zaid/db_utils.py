# db_utils.py

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
        
        res = [dict(row) for row in rows]

        if not res:
            return "No records were found in Database."

        return res

    except Exception as e:
        return f"Error in Database: {str(e)}"

    finally:
        conn.close()