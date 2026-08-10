import sqlite3
from pathlib import Path

DB_PATH = Path("data/ecommerce.db")


def get_connection():
    """
    Returns a connection to the ecommerce SQLite database.
    """

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {DB_PATH}")

    return sqlite3.connect(DB_PATH)