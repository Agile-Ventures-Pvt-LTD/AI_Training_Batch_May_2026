## Support Ticket MCP Server
## Data source: data/tickets.db (SQLite)

from __future__ import annotations
import os
import sqlite3
from typing import Any, Optional, Dict, List
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

class SupportTicketError(RuntimeError):
    """Raised when the ticket database cannot be read or queried."""

mcp = FastMCP(name="support-ticket")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.db")

MAX_RESULT_LIMIT = 50

TICKET_COLUMNS = [
    "ticket_id",
    "service_name",
    "priority",
    "status",
    "subject",
    "description",
    "created_at",
    "customer_impact",
    "assigned_group",
]


def _get_connection() -> sqlite3.Connection:
    """
    Open a connection to the tickets SQLite database.

    Raises:
        SupportTicketError if the database file is missing or cannot be opened.
    """
    if not os.path.exists(DB_PATH):
        raise SupportTicketError(f"Ticket database not found at {DB_PATH}")

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise SupportTicketError(f"Could not open ticket database: {e}")


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {col: row[col] for col in TICKET_COLUMNS if col in row.keys()}


@mcp.tool
def search_tickets(
    service_name: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
) -> Dict[str, Any]:
    """
    Search support tickets using predefined filters.

    Args:
        service_name: Optional service name to filter by (e.g. "Payment API").
        priority: Optional priority to filter by (P1, P2, P3, or P4).
        status: Optional ticket status to filter by (e.g. "OPEN").
        limit: Maximum number of tickets to return (capped at 50).

    Returns:
        A dict with "count" and "tickets", each ticket including
        ticket_id, service_name, priority, status, subject,
        customer_impact, and assigned_group.
    """
    limit = min(max(1, limit), MAX_RESULT_LIMIT)

    query = "SELECT * FROM tickets WHERE 1=1"
    params: List[Any] = []

    if service_name:
        query += " AND service_name = ?"
        params.append(service_name)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if status:
        query += " AND status = ?"
        params.append(status)

    query += " LIMIT ?"
    params.append(limit)

    conn = _get_connection()
    try:
        rows = conn.execute(query, params).fetchall()
    finally:
        conn.close()

    tickets = [
        {
            "ticket_id": r["ticket_id"],
            "service_name": r["service_name"],
            "priority": r["priority"],
            "status": r["status"],
            "subject": r["subject"],
            "customer_impact": r["customer_impact"],
            "assigned_group": r["assigned_group"],
        }
        for r in rows
    ]

    return {
        "count": len(tickets),
        "tickets": tickets,
    }


@mcp.tool
def get_ticket_details(ticket_id: str) -> Dict[str, Any]:
    """
    Get full details of one support ticket.

    Args:
        ticket_id: The unique ticket identifier (e.g. "TKT-1001").

    Returns:
        A dict with "found" and, if found, the full "ticket" record
        including description and created_at.
    """
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        return {
            "found": False,
            "message": "Ticket not found.",
        }

    return {
        "found": True,
        "ticket": _row_to_dict(row),
    }


@mcp.tool
def get_high_priority_tickets(service_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Return open P1 and P2 tickets, optionally filtered by service.

    Args:
        service_name: Optional service name to filter by.

    Returns:
        A dict with "count" and "tickets", each ticket including
        ticket_id, service_name, priority, status, and subject.
    """
    query = "SELECT * FROM tickets WHERE status = 'OPEN' AND priority IN ('P1', 'P2')"
    params: List[Any] = []

    if service_name:
        query += " AND service_name = ?"
        params.append(service_name)

    conn = _get_connection()
    try:
        rows = conn.execute(query, params).fetchall()
    finally:
        conn.close()

    tickets = [
        {
            "ticket_id": r["ticket_id"],
            "service_name": r["service_name"],
            "priority": r["priority"],
            "status": r["status"],
            "subject": r["subject"],
        }
        for r in rows
    ]

    return {
        "count": len(tickets),
        "tickets": tickets,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
