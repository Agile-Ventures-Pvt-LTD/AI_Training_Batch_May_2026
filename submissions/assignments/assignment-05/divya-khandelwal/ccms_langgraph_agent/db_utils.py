import sqlite3

from config import settings



def get_connection():
    """
    Creates and returns SQLite database connection
    """

    conn = sqlite3.connect(
        settings.DB_PATH
    )

    # Return rows as dictionary-like objects
    conn.row_factory = sqlite3.Row

    return conn