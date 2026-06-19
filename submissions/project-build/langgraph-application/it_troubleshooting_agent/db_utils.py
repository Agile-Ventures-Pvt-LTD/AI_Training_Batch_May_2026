from __future__ import annotations

import sqlite3
from typing import Optional

import config


def connect(db_path: Optional[str] = None) -> sqlite3.Connection:
    db_path = db_path or config.DB_PATH
    return sqlite3.connect(db_path)


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    cur = conn.cursor()
    cur.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
    """, (table,))
    return cur.fetchone() is not None
