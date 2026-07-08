"""
db_utils.py
Low-level, parameterized SQLite access helpers for the CCMS agent.
No function here ever accepts or builds raw/arbitrary SQL from user input --
only fixed, parameterized queries are used.
"""

import os
import sqlite3

DB_PATH = os.environ.get("DB_PATH", "data/ccms.db")


def get_connection():
    """Opens a new SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def run_query(query: str, params: tuple = ()) -> list[dict]:
    """
    Executes a single parameterized SELECT query and returns rows as list[dict].
    `query` is always a fixed string literal defined inside tools.py -- never
    built from user-provided text.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def list_tables() -> list[str]:
    """Returns all user table names in the database."""
    rows = run_query("SELECT name FROM sqlite_master WHERE type='table';")
    return [r["name"] for r in rows]


def table_columns(table_name: str) -> list[str]:
    """
    Returns the column names for a given table.
    `table_name` is validated against the real table list before use,
    since PRAGMA does not support parameter binding for identifiers.
    """
    valid_tables = set(list_tables())
    if table_name not in valid_tables:
        return []
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name});")  # table_name is whitelisted above
        return [row[1] for row in cur.fetchall()]
    finally:
        conn.close()


def mask_card_number(card_number: str) -> str:
    """Masks a full card number, showing only the last 4 digits."""
    if not card_number:
        return "N/A"
    digits = "".join(ch for ch in card_number if ch.isdigit())
    if len(digits) < 4:
        return "**** **** **** ****"
    return f"**** **** **** {digits[-4:]}"


def mask_contact(value: str) -> str:
    """Masks emails/phone numbers, keeping only a hint for the user."""
    if not value:
        return "N/A"
    if "@" in value:
        name, domain = value.split("@", 1)
        return f"{name[:2]}***@{domain}"
    return f"***{value[-4:]}" if len(value) > 4 else "****"
