import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "data" / "ecommerce.db"


def get_connection():
    """
    Creates and returns SQLite connection.
    """

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found at: {DB_PATH}"
        )

    conn = sqlite3.connect(DB_PATH)

    return conn