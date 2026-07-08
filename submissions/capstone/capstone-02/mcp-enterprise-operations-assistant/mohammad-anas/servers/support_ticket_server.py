from fastmcp import FastMCP
from pathlib import Path
from src.config import DB_PATH
import sqlite3

mcp = FastMCP("support_ticket_server")

def get_db_connection():
    """Returns a SQLite connection with row access by column name."""
    try:
        path = Path(DB_PATH)
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        return {"error":f"FileNotFoundError {e}"}

@mcp.tool()
def search_tickets(service_name:str=None,priority:str = None, status:str = None, limit:int = 20)-> dict:
    """Search support tickets using predefined filters."""
    conn = get_db_connection()
    query = "SELECT * FROM tickets WHERE 1=1"
    params=[]
    try:
        if service_name:
            query += " AND service_name = ?"
            params.append(service_name)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        if status:
            query += " AND status = ?"
            params.append(status)
    
        safe_limit = min(limit,50)
        query += " LIMIT = ?"
        params.append(safe_limit)
    
        cursor = conn.execute(query,params)
        tickets = [dict(row)for row in cursor.fetchall()]
        conn.close()
    
        return {
            "count":len(tickets),
            "tickets":tickets
        }
    except Exception as e:
        return {"error":f"FileNotFoundError {e}"}

@mcp.tool()
def get_ticket_details(ticket_id:str)-> dict:
    """Get full details of one support ticket."""
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
        row = cursor.fetchone
        conn.close
        if row:
            return{
                "found" : "true",
                "ticket":dict(row)
            }
        return{
            "found":"false",
            "message": "ticket not found"
        }
    except Exception as e:
        return {
            "error":f"error {e}"
        }

@mcp.tool()
def get_high_priority_tickets(service_name:str=None)-> dict:
    conn = get_db_connection()
    try:
        query = "SELECT * FROM WHERE status = 'OPEN' AND priority IN ('P1','P2')"
        params=[]
        if service_name:
            query += " AND services_name = ?"
            params.append(service_name)
        cursor = conn.execute(query,params)
        tickets = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return{
            "count" : len(tickets),
            "tickets" : tickets
        }
    except Exception as e:
        return{
            "error":f"error {e}"
        }

mcp.run()