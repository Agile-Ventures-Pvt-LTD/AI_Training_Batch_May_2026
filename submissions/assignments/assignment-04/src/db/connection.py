import sqlite3

DB_PATH = "data/ecommerce.db"

def get_connection():
    return sqlite3.connect(DB_PATH)