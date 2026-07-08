from pathlib import Path
import sqlite3
from fastmcp import FastMCP


mcp = FastMCP("Support Ticket MCP Server")

DB_PATH = Path(__file__).parent.parent / "data" / "tickets.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

@mcp.tool
def search_tickets(service_name:str = "",priority:str = "",status:str = "",limit:int=20) -> dict:
    """Search support tickets using predefined filters."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT ticket_id, service_name, priority, status, subject, customer_impact, assigned_group FROM tickets WHERE 1=1"
    params = []

    if service_name:
        query += " AND service_name = ?"
        params.append(service_name)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if status:
        query += " AND status = ?"
        params.append(status)

    safe_limit = min(max(limit,1),50)
    query += " LIMIT ?"
    params.append(safe_limit)

    cursor.execute(query,params)
    rows = cursor.fetchall()
    conn.close()

    tickets = [
        {
            "ticket_id": r[0],
            "service_name": r[1],
            "priority": r[2],
            "status": r[3],
            "subject": r[4],
            "customer_impact": r[5],
            "assigned_group": r[6]
        } for r in rows
    ]

    return {"count":len(tickets),"tickets":tickets}

@mcp.tool
def get_ticket_details(ticket_id: str) -> dict:
    """Get full details of one support ticket."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ticket_id, service_name, priority, status, subject, description, created_at, customer_impact, assigned_group FROM tickets WHERE ticket_id = ?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        ticket = {
            "ticket_id": row[0],
            "service_name": row[1],
            "priority": row[2],
            "status": row[3],
            "subject": row[4],
            "description": row[5],
            "created_at": row[6],
            "customer_impact": row[7],
            "assigned_group": row[8]
        }
        return {"found": True, "ticket": ticket}
    return {"found": False, "message": "Ticket not found."}

@mcp.tool
def get_high_priority_tickets(service_name: str = "") -> dict:
    """Return high priority open status tickets"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT ticket_id, service_name, priority, status, subject FROM tickets WHERE status = 'OPEN' AND priority IN ('P1', 'P2')"
    params = []
    
    if service_name:
        query += " AND service_name = ?"
        params.append(service_name)
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    tickets = [
        {
            "ticket_id": r[0],
            "service_name": r[1],
            "priority": r[2],
            "status": r[3],
            "subject": r[4]
        } for r in rows
    ]
    return {"count": len(tickets), "tickets": tickets}

if __name__ == "__main__":
    mcp.run()

