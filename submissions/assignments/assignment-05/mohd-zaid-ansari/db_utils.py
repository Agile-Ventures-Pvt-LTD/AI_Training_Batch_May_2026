# import sqlite3
# from config import db_path


# def get_connection():
#     conn = sqlite3.connect(db_path)
#     return conn


# def execute_query(query, params=None):
#     conn = get_connection()

#     try:
#         cursor = conn.cursor()

#         if params:
#             cursor.execute(query, params)
#         else:
#             cursor.execute(query)

#         rows = cursor.fetchall()

#         return rows

#     finally:
#         conn.close()


import sqlite3
from config import db_path

def get_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query: str, params: tuple = ()):

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

print(execute_query('PRAGMA table_info("transaction")'))