import sqlite3
import os
db_path='data/helpdesk_agent.db'
def validate_db():
    if not os.path.exists(db_path):
        raise Exception(f"Database not found at path: {db_path}")

def get_connection():
    validate_db()
    conn = sqlite3.connect(db_path)
    return conn

def fetch_all(query, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def fetch_one(query, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def execute_write(query, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()