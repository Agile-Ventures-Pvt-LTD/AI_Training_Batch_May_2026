import sqlite3
from config import DB_PATH
import os

print("DB_PATH =", DB_PATH)
print("ABSOLUTE PATH =", os.path.abspath(DB_PATH))
print("FILE EXISTS =", os.path.exists(DB_PATH))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query, params=()):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


def execute_update(query, params=()):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

        return True

    finally:
        conn.close()