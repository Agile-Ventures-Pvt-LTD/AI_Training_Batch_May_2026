# database.py

import sqlite3
from pathlib import Path
from typing import Optional
from pydantic_ai import Agent, RunContext
from agent import travel_agent

DB_PATH = Path(__file__).parent.parent.parent / "db" / "travel_data.db"

@travel_agent.tool
def get_user_bookings(identifier: str) -> list[dict]:
    """
    Get bookings by email or booking_id .
    
    Args:
        identifier: User email (e.g., 'zaid@email.com') or booking ID (e.g., 'TRV-101')
    
    Returns:
        List of booking dictionaries.
    """
    if not DB_PATH.exists():
        return [{"error": "Database file not found"}]
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
        # for searching with Booking ID
        if identifier.upper().startswith("TRV-"):
            cursor.execute(
                "SELECT destination FROM bookings WHERE booking_id = ?",
                (identifier.upper(),)
            )
        # for searching with Booking email
        else:
            cursor.execute(
                "SELECT destination FROM bookings WHERE user_email = ?",
                (identifier.strip().lower(),)
            )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except Exception as e:
        return [{"Error": f"Database error: {str(e)}"}]
    