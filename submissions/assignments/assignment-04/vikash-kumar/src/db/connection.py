import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "data" / "ecommerce.db"


def get_connection():
    """
    Creates and returns a SQLite connection.
    """

    try:
        conn = sqlite3.connect(DB_PATH)

        conn.row_factory = sqlite3.Row

        return conn

    except sqlite3.Error as e:
        raise Exception(
            f"Database connection failed: {str(e)}"
        )