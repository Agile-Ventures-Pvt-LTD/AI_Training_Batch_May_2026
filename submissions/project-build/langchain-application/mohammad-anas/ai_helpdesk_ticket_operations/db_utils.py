import sqlite3
from config import DB_PATH

def set_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con
def read_db(query, params=()):
    """Reads datas from the database safely."""
    try:
        with set_db() as con:
            cursor = con.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        err = {"error": str(e)}
        return err

def write_db(query, params=(), tool_name="unknown", input_data=""):
    """Executes updates or inserts and logs the action ."""
    try:
        with set_db() as con:
            cursor = con.cursor()
            cursor.execute(query, params)
            audit_query = """
                INSERT INTO tool_audit_logs (tool_name, input, output, status) 
                VALUES (?, ?, ?, 'SUCCESS')
            """
            cursor.execute(audit_query, (tool_name, str(input_data), "Operation completed"))
            con.commit()
            return {"status": "success"}
    except Exception as e:
        err ={"error": str(e), "status": "failed"}
        return err