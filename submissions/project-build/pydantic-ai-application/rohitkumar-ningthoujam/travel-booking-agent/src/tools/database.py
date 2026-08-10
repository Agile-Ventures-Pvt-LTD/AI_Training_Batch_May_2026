import os
import sqlite3
from pydantic_ai import Agent
from dotenv import load_dotenv
load_dotenv()
from Agent import input_query
DB_PATH = os.getenv("DB_PATH", "db/travel_data.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        rows = [dict(r) for r in rows]
    except Exception as e:
        rows = []
        print("DB Error:", e)

    conn.close()
    return rows
@agent.tool
async def user_information(
    id: int = None,
    booking_id: str = None,
    user_name : str = None,
    user_email: str = None,
    destination : str = None,
    travel_dates : str = None,
    hotel_details : str = None
):
    """find the user information"""

    input_query = """
    SELECT *
    FROM bookings
    WHERE 1=1
    """

    params = []

    if id is not None:
        try:
            id = int(id)
        except (ValueError, TypeError):
            pass
        input_query += " AND id = ?"
        params.append(id)
    if booking_id is not None:
        try:
            booking_id = int(booking_id)
        except (ValueError, TypeError):
            pass
        input_query += " AND booking_id = ?"
        params.append(booking_id)    


    if user_email:
        input_query += " AND user_email = ?"
        params.append(user_email)

    if destination:
        input_query += " AND destination = ?"
        params.append(destination)

    if user_name:
        input_query += " AND user_name ?"
        params.append(f"%{user_name}%")
    if travel_dates:
        input_query += " AND travel_dates ?"
        params.append(f"%{travel_dates}%")

    if hotel_details:
        input_query += " AND hotel_details?"
        params.append(f"%{hotel_details}%")


    result = execute_query(input_query, tuple(params))

    if not result:
        return {"found": False, "booking": None}

    row = result[0]

    
    return {
        "found": True,
        "booking": {
            "id": row["id"],
            "user_name": row["user_name"],
            "user_email":row["user_email"],
            "destination": row["destination"],
            "booking_id": row["city"],
            "travel_dates": row["travel_dates"],
            "hotel_details" : row["hotel_details"]
        }
    }
      

    


