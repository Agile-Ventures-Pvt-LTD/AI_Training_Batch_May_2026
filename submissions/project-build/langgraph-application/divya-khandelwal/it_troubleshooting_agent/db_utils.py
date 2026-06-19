import sqlite3

from config import settings

def get_connection():
    """
    Creates and returns SQLite database connection
    """
    conn = sqlite3.connect(
        settings.DB_PATH
    )
    conn.row_factory = sqlite3.Row
    print("DB connected")
    return conn

if __name__=="__main__":
    get_connection()