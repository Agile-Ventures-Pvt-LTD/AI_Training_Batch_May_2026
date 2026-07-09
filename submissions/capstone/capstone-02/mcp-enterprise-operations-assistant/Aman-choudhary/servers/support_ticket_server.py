from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any
from fastmcp import FastMCP
mcp = FastMCP("Support Ticket MCP Server")
DB_FILE = Path("data/tickets.db")
MAX_LIMIT = 50
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row)
@mcp.tool
def search_tickets(service_name: str | None = None,priority: str | None = None,status: str | None = None,limit: int = 20,)-> dict:
    """
    Search support  
    """
    limit = min(limit, MAX_LIMIT)
    query = "select * from ticket where 1==1"
    params: list[Any] = []
    if service_name:
        query += " AND service_name = ?"
        params.append(service_name)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY created_at desc limit ?"
    params.append(limit)
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    tickets = [row_to_dict(row) for row in rows]
    return {"count": len(tickets),"tickets": tickets,}
@mcp.tool
def get_ticket_details(ticket_id: str) -> dict:
    """
    Return complete details of a ticket.
    """
    with get_connection() as conn:
        row = conn.execute(
            """ select * from ticket where ticket_id=?""",(ticket_id,),).fetchone()
    if row is None:
        return {"found": False,"message": "Ticket not found.",}
    return {"found": True,"ticket": row_to_dict(row),}


@mcp.tool
def get_high_priority_tickets(service_name: str | None = None,)-> dict:
     
    query = """select ticket_id,service_name,priority,status,subject from ticket where status="open" and prority in ('p1','p2') """

    params: list[Any] = []
    if service_name:
        query += " AND service_name = ?"
        params.append(service_name)
    query += " ORDER BY created_at DESC"
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    tickets = [row_to_dict(row) for row in rows]
    return {"count": len(tickets),"tickets": tickets,}


if __name__ == "__main__":
    mcp.run()