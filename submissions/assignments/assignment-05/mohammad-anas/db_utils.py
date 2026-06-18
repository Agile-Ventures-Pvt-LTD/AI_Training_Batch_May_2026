import sqlite3
from config import DB_PATH

def get_connection():
    """Return a sqlite3.Connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row):
    if not row:
        return None
    
    return {k : row[k] for k in row.keys()}

def execute(query,params=(), commit= False):
    """Execute a write query safely. Returns number of affected rows."""
    conn = get_connection()
    
    try:
        cur = conn.execute(query,params)
        if commit:
            conn.commit()
        return cur.rowcount
    except Exception as e:
        return f"error: {e}"
        
    finally:
        conn.close()
        
def fetch_one(query,params=()):
    """fetch a single row as a dict"""
    conn = get_connection()
    
    try:
        cur = conn.execute(query,params)
        res = row_to_dict(cur.fetchone())
        return res
    except Exception as e:
        print(f"DB Error in fetch_one: {e}")
        return None
    finally:
        conn.close()
        
def fetch_all(query, params=()):
    """Fetch multiple rows as list of dicts"""
    conn = get_connection()
    try:
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return [row_to_dict(r) for r in rows]
    except Exception as e:
        print(f" DB Error in fetch_one: {e}")
        return None
    finally:
        conn.close()

def inspect_schema():
    """Return a list of table names (excluding sqlite internal tables)."""
    q = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    rows = fetch_all(q)
    return [r["name"] for r in rows] 