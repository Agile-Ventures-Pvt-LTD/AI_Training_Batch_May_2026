import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional

DB_PATH = Path("db/travel_data.db")

def get_connection(db_path: str = str(DB_PATH)) -> sqlite3.Connection:
    path = Path(db_path)
    if not path.exists():
        alternative_path = Path(__file__).parent.parent.parent / "db" / "travel_data.db"
        if alternative_path.exists():
            path = alternative_path
        else:
            raise FileNotFoundError(f"Database not found at: {path}")    
    
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def query_booking(identifier: str, db_path: str = str(DB_PATH)) -> Optional[Dict[str, Any]]:
    """
    Query the bookings table in SQLite database using either user_email or booking_id.
    
    Args:
        identifier: User email (contains '@') or booking_id (e.g. 'TRV-101')
        db_path: Path to the SQLite database
        
    Returns:
        A dictionary containing booking details if found, else None.
    """
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()
        identifier = identifier.strip()
        
        if "@" in identifier:
            cursor.execute("SELECT * FROM bookings WHERE user_email = ?", (identifier,))
        else:
            cursor.execute("SELECT * FROM bookings WHERE booking_id = ?", (identifier,))
            
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except Exception as e:
        raise RuntimeError(f"Database error: {str(e)}")

SCHEMA_DESCRIPTION="""

TABLE: bookings
id INTEGER PRIMARY KEY
booking_id TEXT UNIQUE
user_name TEXT 
user_email TEXT
destination TEXT
travel_dates TEXT
hotel_details TEXT

"""
