import sqlite3
from config import DB_PATH
def get_connection():
    return sqlite3.connect(
        DB_PATH
    )
    
def inspect_schema():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    )

    tables = [
        row[0]
        for row in cursor.fetchall()
    ]

    schema = {}
    for table in tables:
        cursor.execute(
            f"PRAGMA table_info({table})"
        )

        schema[table] = [
            column[1]
            for column in cursor.fetchall()
        ]

    conn.close()

    return {
        "tables": tables,
        "schema": schema
    }