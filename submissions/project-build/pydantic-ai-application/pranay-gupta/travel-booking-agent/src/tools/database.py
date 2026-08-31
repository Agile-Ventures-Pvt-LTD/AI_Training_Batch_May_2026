import json
import sqlite3

def get_db_connection():
    conn = sqlite3.connect(r"db\travel_data.db")
    conn.row_factory = sqlite3.Row
    return conn

def execute_select_query(query: str,params: tuple=()):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query,params)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]

        if not result:
            return "No Records found"
        
        return json.dumps(result, indent=2)

    except Exception as e:
        return f"Database Error: {str(e)}"

    finally:
        conn.close()

def get_details(booking_id):
    """Get All traveling details using booking_id"""

    query = """
            SELECT user_name, user_email, destination, travel_dates, hotel_details
            FROM bookings WHERE booking_id = ?
            """

    return execute_select_query(query,(booking_id,))

