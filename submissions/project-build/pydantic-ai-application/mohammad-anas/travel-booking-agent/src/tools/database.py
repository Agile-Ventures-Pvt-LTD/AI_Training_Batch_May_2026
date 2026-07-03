import sqlite3
from typing import List, Dict, Any
from pathlib import Path
from pydantic import BaseModel

DB_PATH = Path(__file__).resolve().parents[2] / "db" / "travel_data.db"


class Booking(BaseModel):
    booking_id: str
    user_name: str
    user_email: str
    destination: str
    travel_dates: str
    hotel_details: str


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def _row_to_booking(row: sqlite3.Row) -> Booking:
    return Booking(
        booking_id=row["booking_id"],
        user_name=row["user_name"],
        user_email=row["user_email"],
        destination=row["destination"],
        travel_dates=row["travel_dates"],
        hotel_details=row["hotel_details"],
    )


def get_upcoming_booking(identifier: str,) -> Booking | None:
    conn = _connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if "@" in identifier:
        query = """
            SELECT * FROM bookings
            WHERE user_email = ?
            ORDER BY id ASC LIMIT 1
        """
    else:
        query = """
            SELECT * FROM bookings
            WHERE booking_id = ?
            ORDER BY id ASC LIMIT 1
        """

    cur.execute(query, (identifier,))
    row = cur.fetchone()
    conn.close()
    return _row_to_booking(row) if row else None