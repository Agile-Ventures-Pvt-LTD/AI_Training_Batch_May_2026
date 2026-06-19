import sqlite3
from utils.paths import db_path

def get_conn(DB_PATH=db_path):
    try:
        return sqlite3.connect(DB_PATH)
    except Exception as e:
        print(f"Error: {e}")