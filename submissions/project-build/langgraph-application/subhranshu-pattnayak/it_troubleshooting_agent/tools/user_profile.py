from db_utils.db_connection import get_conn
import sqlite3
from langchain.tools import tool

@tool
def get_user_profile_tool(user_id, full_name, email):
    '''
    Fetches user profile from database.
    '''
    
    try:
        conn=get_conn()
        conn.row_factory=sqlite3.Row
        cursor=conn.cursor()

        if user_id:
            query = "SELECT * FROM users WHERE user_id=?"
            params = [user_id]
        elif email:
            query = "SELECT * FROM users WHERE email=?"
            params = [email]
        elif full_name:
            query = "SELECT * FROM users WHERE full_name LIKE ?"
            params = [f"%{full_name}%"]
        else:
            conn.close()
            return None

        cursor.execute(query,params)
        row = cursor.fetchone()
        conn.close()
        return dict(row)
    
    except Exception as e:
        print(F"Error: {e}")
        return None