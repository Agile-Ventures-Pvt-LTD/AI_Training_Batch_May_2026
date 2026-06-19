from db_utils.db_connection import get_conn
import sqlite3
from langchain.tools import tool

@tool
def get_device_status_tool(user_id):
    """Fetches device statuses for user devices.
    """
    try:
        conn=get_conn()
        conn.row_factory=sqlite3.Row
        cursor=conn.cursor()

        if user_id:
            query = "SELECT * FROM devices WHERE user_id=?"
            params = [user_id]
        else:
            conn.close()
            return None

        cursor.execute(query,params)
        row = cursor.fetchall()
        conn.close()
        return row
    
    except Exception as e:
        print(F"Error: {e}")
        return None