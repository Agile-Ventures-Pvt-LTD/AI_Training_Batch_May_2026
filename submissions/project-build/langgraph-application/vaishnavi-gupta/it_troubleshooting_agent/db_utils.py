import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List
from config import DB_PATH

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()


def execute_query(
    query: str,
    params: tuple = ()
) -> List[Dict[str, Any]]:
    """
    Execute parameterized SELECT query.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(query, params)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]


def execute_single(
    query: str,
    params: tuple = ()
) -> Dict[str, Any] | None:

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(query, params)

        row = cursor.fetchone()

        return dict(row) if row else None


def get_all_tables() -> List[str]:

    query = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """

    rows = execute_query(query)

    return [row["name"] for row in rows]


def get_table_schema(table_name: str):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            f'PRAGMA table_info("{table_name}")'
        )

        columns = cursor.fetchall()

        return [dict(col) for col in columns]