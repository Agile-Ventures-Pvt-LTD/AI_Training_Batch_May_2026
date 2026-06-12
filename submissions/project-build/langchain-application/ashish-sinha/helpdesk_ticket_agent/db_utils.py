import sqlite3
from config import DB_Path


def getting_connection():

    conn = sqlite3.connect(DB_Path)
    conn.row_factory = sqlite3.Row

    return conn

def fetching_all(query:str,params:tuple=()):
    conn = getting_connection()

    try:
        cursor =conn.cursor()
        cursor.execute(query,params)
        rows=cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def fetching_one(query:str,params:tuple = ()):
    conn = getting_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query,params)
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()

def execution_query(query:str,params:tuple = ()):
    conn = getting_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query,params)
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()
