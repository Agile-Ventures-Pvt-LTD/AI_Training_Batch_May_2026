import sqlite3
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("Support Ticket MCP Server")

def get_db_connection():
    db_path = Path(__file__).resolve().parents[1] / "data" / "tickets.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@mcp.tool
def search_tickets(service_name: str | None = None, priority: str | None = None, status: str | None = None, limit: int = 50) -> dict:
    """Search support tickets using predefined filters.
    
    Args:
        service_name: Optional name of the service to filter by.
        priority: Optional priority level (e.g., P1, P2, P3, P4).
        status: Optional ticket status (e.g., OPEN, RESOLVED).
        limit: Maximum number of results to return (capped at 50).
        
    Returns:
        A dictionary containing count and list of tickets.
    """
    limit = min(max(1, limit), 50)
    query = "SELECT ticket_id, service_name, priority, status, subject, customer_impact, assigned_group FROM tickets"
    where_clauses = []
    params = []
    
    if service_name:
        where_clauses.append("service_name = ?")
        params.append(service_name)
    if priority:
        where_clauses.append("priority = ?")
        params.append(priority)
    if status:
        where_clauses.append("status = ?")
        params.append(status)
        
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
        
    query += " LIMIT ?"
    params.append(limit)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        tickets = [dict(row) for row in rows]
        
    return {
        "count": len(tickets),
        "tickets": tickets
    }

@mcp.tool
def get_ticket_details(ticket_id: str) -> dict:
    """Get full details of one support ticket.
    
    Args:
        ticket_id: The unique identifier of the ticket (e.g., TKT-1001).
        
    Returns:
        Detailed ticket information if found, or a failure message.
    """
    query = "SELECT ticket_id, service_name, priority, status, subject, description, created_at, customer_impact, assigned_group FROM tickets WHERE ticket_id = ?"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (ticket_id,))
        row = cursor.fetchone()
        
    if row:
        return {
            "found": True,
            "ticket": dict(row)
        }
    return {
        "found": False,
        "message": "Ticket not found."
    }

@mcp.tool
def get_high_priority_tickets(service_name: str | None = None) -> dict:
    """Return open P1 and P2 tickets. The tool may optionally filter by service.
    
    Args:
        service_name: Optional name of the service to filter by.
        
    Returns:
        A dictionary containing count and list of high priority open tickets.
    """
    query = "SELECT ticket_id, service_name, priority, status, subject FROM tickets WHERE priority IN ('P1', 'P2') AND status = 'OPEN'"
    params = []
    if service_name:
        query += " AND service_name = ?"
        params.append(service_name)
        
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        tickets = [dict(row) for row in rows]
        
    return {
        "count": len(tickets),
        "tickets": tickets
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
