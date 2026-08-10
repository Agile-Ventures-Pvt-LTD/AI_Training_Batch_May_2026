import sqlite3
import time
from pathlib import Path
from langchain.tools import tool

@tool
def _get_db_path(db_path=None):
    if db_path:
        return Path(db_path)
    # default to a local file next to the project
    return Path("agent_memory.db")

@tool
def _ensure_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS agent_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            created_at INTEGER
        )
        """
    )

@tool
def add_message(role, content, db_path=None):
    path = _get_db_path(db_path)
    conn = sqlite3.connect(path)
    try:
        _ensure_table(conn)
        conn.execute(
            "INSERT INTO agent_memory(role, content, created_at) VALUES (?, ?, ?)",
            (role, content, int(time.time())),
        )
        conn.commit()
    finally:
        conn.close()

@tool
def get_recent(limit=20, db_path=None):
    path = _get_db_path(db_path)
    conn = sqlite3.connect(path)
    try:
        _ensure_table(conn)
        cur = conn.execute(
            "SELECT role, content, created_at FROM agent_memory ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
        # return in chronological order
        return [dict(role=r[0], content=r[1], ts=r[2]) for r in reversed(rows)]
    finally:
        conn.close()

@tool
def clear_memory(db_path=None):
    path = _get_db_path(db_path)
    conn = sqlite3.connect(path)
    try:
        _ensure_table(conn)
        conn.execute("DELETE FROM agent_memory")
        conn.commit()
    finally:
        conn.close()


TOOL2=[_ensure_table,_get_db_path,get_recent,clear_memory]