import os
import sqlite3
try:
    from config import DATA_DIR
except ImportError:
    from .config import DATA_DIR

DB_PATH = os.path.join(DATA_DIR, "travel_data.db")

def get_connection():
    return sqlite3.connect(DB_PATH)