import sqlite3
import sys
from fastmcp import FastMCP
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import TICKETS_DB

sts_mcp = FastMCP("Support Ticket MCP Server")


def _dict_factory(cursor, row):
    fields = [col[0] for col in cursor.description]
    return {fields[i]: row[i] for i in range(len(fields))}


def _query_db(query: str, params: tuple = ()) -> list:
    if not TICKETS_DB.exists():
        return []
    with sqlite3.connect(TICKETS_DB) as conn:
        conn.row_factory = _dict_factory
        return conn.execute(query, params).fetchall()


@sts_mcp.tool
def search_tickets(service_name: str = None, status: str = None, priority: str = None, limit: int = 20) -> dict:
    """Search support tickets using predefined filters."""
    limit = min(max(int(limit), 1), 50)
    sql = "SELECT ticket_id, service_name, priority, status, subject, customer_impact, assigned_group FROM tickets WHERE 1=1"
    args = []

    if service_name:
        sql += " AND LOWER(service_name) = LOWER(?)"
        args.append(service_name)
    if status:
        sql += " AND LOWER(status) = LOWER(?)"
        args.append(status)
    if priority:
        sql += " AND LOWER(priority) = LOWER(?)"
        args.append(priority)

    sql += " LIMIT ?"
    args.append(limit)

    results = _query_db(sql, tuple(args))
    return {"count": len(results), "tickets": results}


@sts_mcp.tool
def get_ticket_details(ticket_id: str) -> dict:
    """Get full details of one support ticket."""
    sql = "SELECT * FROM tickets WHERE LOWER(ticket_id) = LOWER(?)"
    rows = _query_db(sql, (ticket_id,))
    if rows:
        return {"found": True, "ticket": rows[0]}
    return {"found": False, "message": "Ticket not found."}


@sts_mcp.tool
def get_high_priority_tickets(service_name: str = None) -> dict:
    """Return open P1 and P2 tickets, optionally filtered by service."""
    sql = "SELECT ticket_id, service_name, priority, status, subject FROM tickets WHERE status = 'OPEN' AND priority IN ('P1', 'P2')"
    args = []

    if service_name:
        sql += " AND LOWER(service_name) = LOWER(?)"
        args.append(service_name)

    results = _query_db(sql, tuple(args))
    return {"count": len(results), "tickets": results}


if __name__ == "__main__":
    sts_mcp.run()