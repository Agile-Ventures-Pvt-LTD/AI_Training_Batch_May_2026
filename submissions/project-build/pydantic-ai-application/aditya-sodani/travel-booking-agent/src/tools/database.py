import sqlite3
import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from src.config import *
from src.agent import agent



#Database Tool


class TripQueryInput(BaseModel):
    identifier: str = Field(..., description="User email or booking ID")

class TripDetails(BaseModel):
    destination_city: str
    start_date: str
    end_date: str
    hotel_name: str

@agent.tool
def get_upcoming_trip(ctx: RunContext,data: TripQueryInput) -> List[TripDetails]:
    """
    Retrieves upcoming travel plans for a given user from travel_data.db.
    """
    trips = []
    try:
        conn = sqlite3.connect("db/travel_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT destination, travel_dates, hotel_details
            FROM bookings
            WHERE (user_email = ? OR booking_id = ?)
              AND date(start_date) >= date('now')
            ORDER BY start_date ASC
            LIMIT 1
        """, (data.identifier, data.identifier))
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            trips.append(TripDetails(
                destination_city=row[0],
                start_date=row[1],
                end_date=row[2],
                hotel_name=row[3]
            ))
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")

    if not trips:
        raise ValueError("No upcoming trips found for this identifier.")

    return trips

