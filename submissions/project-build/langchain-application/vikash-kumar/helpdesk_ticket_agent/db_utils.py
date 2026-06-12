import sqlite3
from contextlib import contextmanager

from config import DATABASE_PATH


@contextmanager
def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    try:
        yield connection

    finally:
        connection.close()


def execute_select_query(query: str, params: tuple = ()):
    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(query, params)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]


def execute_single_record_query(query: str,params: tuple = ()):

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(query, params)

        row = cursor.fetchone()

        if row:
            return dict(row)

        return None


def execute_update_query(query: str, params: tuple = ()):
    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

        return cursor.rowcount


def table_exists(table_name: str):
    
    query = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name=?
    """

    result = execute_single_record_query(query,(table_name,))

    return result is not None


def get_database_statistics():

    tables = [
        "tickets",
        "customers",
        "ticket_comments",
        "conversation_logs",
        "conversation_summaries",
        "archival_memory",
        "tool_audit_logs"
    ]

    stats = {}

    for table in tables:

        if table_exists(table):

            query = f"""
            SELECT COUNT(*) AS total
            FROM {table}
            """

            result = execute_single_record_query(query)

            stats[table] = result["total"]

    return stats


def validate_database():

    required_tables = [
        "tickets",
        "customers",
        "ticket_comments",
        "conversation_logs",
        "conversation_summaries",
        "archival_memory",
        "tool_audit_logs"
    ]

    missing_tables = []

    for table in required_tables:

        if not table_exists(table):
            missing_tables.append(table)

    return {
        "valid": len(missing_tables) == 0,
        "missing_tables": missing_tables
    }