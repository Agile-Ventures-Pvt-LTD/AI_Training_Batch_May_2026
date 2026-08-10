import sqlite3

from config import DB_PATH


def get_connection():
    connection = sqlite3.connect(DB_PATH)

    # Allows row access by column name
    connection.row_factory = sqlite3.Row

    return connection


def fetch_one(query, params=()):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def fetch_all(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def inspect_schema():
    query = """
    SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """
    return fetch_all(query)

def execute_query(query, params=()):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()