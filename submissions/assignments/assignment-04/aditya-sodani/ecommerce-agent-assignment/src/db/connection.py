import sqlite3

DATABASE_PATH = "data/ecommerce.db"

def get_connection():
    return sqlite3.connect(DATABASE_PATH)