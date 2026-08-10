import sqlite3

DB_PATH = "data/helpdesk_agent.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

# from database.connection import get_connection