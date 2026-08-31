import sqlite3
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from database_pydantic_ai import (
    SQLiteDatabase,
    SQLDatabaseDeps,
    SQLITE_SYSTEM_PROMPT,
    create_database_toolset,
)
import sys
db_path = os.getenv('DB_PATH')

class BookingDetails(BaseModel):
    booking_id: str 
    user_name: str 
    user_email: str 
    destination: str 
    travel_dates: str
    hotel_details: str

# async def main():
#     async with SQLiteDatabase("data.db") as db:
#         deps = SQLDatabaseDeps(database=db, read_only=True)
#         toolset = create_database_toolset()

def fetch_booking_from_db(db_path:str, identifier: str) -> Optional[Dict[str, Any]]:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    query = """
        SELECT booking_id, user_name, user_email, destination, travel_dates, hotel_details 
        FROM bookings 
        WHERE booking_id = ? OR user_email = ?
        LIMIT 1
    """
    
    try:
        cursor.execute(query, (identifier, identifier))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except sqlite3.Error as error:
        print(f"Database extraction failure trace: {error}", file=sys.stderr)
        return None
    finally:
        connection.close()
