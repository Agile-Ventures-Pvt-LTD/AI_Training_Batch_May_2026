import sqlite3
from dotenv import load_dotenv
load_dotenv()
import os
DB_URI=os.getenv("DB_URI")


def get_db():
    database_path=DB_URI
    connection=sqlite3.connect(database_path)
    return connection

def get_details(user_name: str = None,user_email: str = None,booking_id: str = None):
    """ This tool is used to get user details .Find users information by user ID, email, or full name"""
    query = None
    params = ()

    if user_name:
        query = "SELECT * FROM bookings WHERE user_name = ?"
        params = (user_name,)

    elif user_email:
        query = "SELECT * FROM bookings WHERE user_email = ?"
        params = (user_email,)

    elif booking_id:
        query = " SELECT * FROM bookings WHERE booking_id = ?"
        params = ("booking_id",)

    else:
        return {
            "found": False,
            "message": "No search criteria provided."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        user = cursor.fetchone()
        if not user:
            return {
                "found": False,
                "user": None
            }
        return {
            "found": True,
            "user": {
                "user_id": user["id"],
                "booking_id": user["booking_id"],
                "user_name": user["user_name"],
                "user_email": user["user_email"],
                "destination": user["destination"],
                "travel_dates": user["travel_dates"],
                "hotel_details": user["hotel_details"]
            }
        }

    finally:
        conn.close()