"""
connection.py

Purpose:
--------
Centralized SQLite database connection management.

Used by:
---------
- SQL Tool
- Agent
- Tests
- Future Reporting Modules
"""

import sqlite3
from pathlib import Path


# Project Paths

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DB_PATH = PROJECT_ROOT / "data" / "ecommerce.db"


# Database Existence Check

def database_exists() -> bool:
    """
    Check whether ecommerce.db exists.

    Returns:
        bool
    """

    return DB_PATH.exists()

# Create Database Connection

def get_connection() -> sqlite3.Connection:
    """
    Create and return SQLite connection.

    Returns:
        sqlite3.Connection

    Raises:
        FileNotFoundError
        sqlite3.Error
    """

    if not database_exists():

        raise FileNotFoundError(
            f"Database not found:\n{DB_PATH}"
        )

    try:

        connection = sqlite3.connect(DB_PATH)

        # Enable foreign key constraints
        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    except sqlite3.Error as error:

        raise sqlite3.Error(
            f"Database connection failed: {error}"
        )

# Database Health Check

def test_connection() -> bool:
    """
    Verify database is accessible.

    Returns:
        True if healthy
    """

    try:

        conn = get_connection()

        conn.execute(
            "SELECT 1"
        )

        conn.close()

        return True

    except Exception:

        return False


# Execute Read Query

def execute_query(query: str):
    """
    Execute SELECT query and return
    list of dictionaries.
    """

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    results = [
        dict(row)
        for row in rows
    ]

    conn.close()

    return results


# Get Table Names

def get_table_names():
    """
    Returns all table names.
    """

    query = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """

    tables = execute_query(query)

    return [
        table["name"]
        for table in tables
    ]


# Get Schema

def get_table_schema(table_name: str):
    """
    Returns schema details for a table.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    schema = cursor.fetchall()

    conn.close()

    return schema


# Show Database Summary

def database_summary():
    """
    Prints table names and row counts.
    """

    tables = get_table_names()

    print("\nDATABASE SUMMARY")
    print("=" * 50)

    conn = get_connection()

    cursor = conn.cursor()

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(
            f"{table:<15} {count}"
        )

    conn.close()


# Run Standalone

if __name__ == "__main__":

    print(
        f"Database Exists: {database_exists()}"
    )

    print(
        f"Connection Healthy: {test_connection()}"
    )

    database_summary()