import sqlite3
from langchain_core.tools import tool

from .db_config import DB_PATH


@tool
def execute_sql(query: str, db_path: str = DB_PATH) -> str:
    """
    Execute a read-only SQL query against the SQLite database.
    """

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        conn.close()

        return str({
            "columns": columns,
            "rows": rows
        })

    except Exception as e:
        return f"SQL Error: {e}"


@tool
def get_schema(db_path: str = DB_PATH) -> str:
    """
    Return database schema information.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = cursor.fetchall()

    schema = []

    for (table,) in tables:
        cursor.execute(f"PRAGMA table_info({table})")

        cols = cursor.fetchall()

        schema.append(
            f"{table}: " +
            ", ".join(col[1] for col in cols)
        )

    conn.close()
    return "\n".join(schema)