import sqlite3
import os
from typing import List, Dict, Any

class SQLProductDatabase:
    """A direct SQLite database client simulating a relational travel bookings catalog."""
    
    def __init__(self, db_path: str = "db/travel_data.db"):
        self.db_path = db_path
        
    def query_db(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """General read-only query helper. Restricts write actions for safety."""
        query_upper = query.upper()
        for forbidden in ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]:
            if forbidden in query_upper:
                raise PermissionError(f"Write or modification queries like '{forbidden}' are strictly prohibited.")
                
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
            
    def get_users(self) -> List[Dict[str, Any]]:
        """Retrieve all users in db."""
        return self.query_db("SELECT id, booking_id, user_name, user_email, destination, travel_dates, hotel_details FROM bookings")
        
    def get_user_by_name(self, name: str) -> Dict[str, Any]:
        """Lookup user details by name (case-insensitive fuzzy matching)."""
        res = self.query_db("SELECT id, booking_id, user_name, user_email, destination, travel_dates, hotel_details FROM bookings WHERE user_name LIKE ?", (f"%{name}%",))
        return res[0] if res else {}
        
    def get_user_travels(self, user_name: str) -> List[Dict[str, Any]]:
        """Retrieve travel data for a customer."""
        return self.query_db("SELECT id, booking_id, user_name, destination, travel_dates, hotel_details FROM bookings WHERE user_name LIKE ?", (f"%{user_name}%",))




# Project: P005 RAG Ecommerce support chatbot
# Author: Poonam Bhatt