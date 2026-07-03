db_path="db/travel_data.db"
import sqlite3
from src.agent import agent
from pydantic_ai import Agent, RunContext

def get_connection():
    conn=sqlite3.connect(db_path)
    conn.row_factory=sqlite3.Row
    return conn

def execute_query(query:str, params: tuple=()):
    conn=get_connection()
    try:
        cursor=conn.cursor()
        cursor.execute(query, params)
        rows=cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

print(execute_query('PRAGMA table_info(bookings)'))

#================================================================================================================================

@agent.tool
def get_travel_plan(booking_id:RunContext[str]) -> str:
    """You have to get the details of user travelling details like user_name, user_email, destinaation, travel_date, destination and hotel_details."""

    query="""SELECT id, user_name, user_email, destination, travel_dates, hotel_details from bookings
    WHERE booking_id=?"""

    return execute_query(query, (booking_id,))


