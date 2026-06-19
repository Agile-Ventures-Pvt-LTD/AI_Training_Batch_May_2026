import sqlite3
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

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

    tables = [row[0] for row in cursor.fetchall()]

    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        schema[table] = [column[1] for column in cursor.fetchall()]

    conn.close()

    return {
        "tables": tables,
        "schema": schema,
    }


def query_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()
    if row:
        return dict(zip(columns, row))
    return None


def query_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,))
    row = cursor.fetchone()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()
    if row:
        return dict(zip(columns, row))
    return None


def query_user_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE LOWER(full_name) LIKE LOWER(?)",
        (f"%{name}%",),
    )
    row = cursor.fetchone()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()
    if row:
        return dict(zip(columns, row))
    return None


def query_device_by_user_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()
    if row:
        return dict(zip(columns, row))
    return None


def query_known_incidents(service_name=None, region=None, status="Active"):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM known_incidents WHERE 1=1"
    params = []

    if service_name:
        sql += " AND LOWER(service_name) LIKE LOWER(?)"
        params.append(f"%{service_name}%")
    if region:
        sql += " AND LOWER(region) LIKE LOWER(?)"
        params.append(f"%{region}%")
    if status:
        sql += " AND LOWER(status) = LOWER(?)"
        params.append(status)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()

    return [dict(zip(columns, row)) for row in rows]


def query_diagnostic_snapshot(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM diagnostic_snapshots
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (user_id,),
    )
    row = cursor.fetchone()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()
    if row:
        return dict(zip(columns, row))
    return None


def query_ticket_by_id(ticket_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    row = cursor.fetchone()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()
    if row:
        return dict(zip(columns, row))
    return None


def query_tickets_by_user_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tickets WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    )
    rows = cursor.fetchall()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()
    return [dict(zip(columns, row)) for row in rows]


def search_tickets(keyword=None, issue_type=None, status=None):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if keyword:
        sql += " AND (LOWER(subject) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?))"
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    if issue_type:
        sql += " AND LOWER(issue_type) = LOWER(?)"
        params.append(issue_type)
    if status:
        sql += " AND LOWER(status) = LOWER(?)"
        params.append(status)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()

    return [dict(zip(columns, row)) for row in rows]


def get_all_active_incidents():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM known_incidents WHERE LOWER(status) = 'active'")
    rows = cursor.fetchall()
    columns = [d[0] for d in cursor.description] if cursor.description else []
    conn.close()
    return [dict(zip(columns, row)) for row in rows]


def initialize_database():
    import os
    if os.path.exists(DB_PATH):
        return
    conn = get_connection()
    conn.close()
