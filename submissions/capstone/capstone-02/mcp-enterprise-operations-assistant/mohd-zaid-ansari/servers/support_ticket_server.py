import argparse
import asyncio
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data"

db_path = DATASET_PATH / "tickets.db"

mcp = FastMCP()


def get_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query: str, params: tuple = ()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@mcp.tool
async def search_tickets(service_name: str = None,priority: str = None,status: str = None,limit: int = 20,) -> Dict[str, Any]:
    """Search support tickets using predefined filters."""

    query = """SELECT ticket_id, service_name, priority, status, subject, customer_impact, assigned_group 
            FROM tickets WHERE 1=1 """

    params: List[Any] = []

    if service_name:
        query += "AND service_name=? "
        params.append(service_name)
    if priority:
        query += "AND priority=? "
        params.append(priority)
    if status:
        query += "AND status=? "
        params.append(status)
    if limit is None:
        limit = 20
    limit = min(int(limit), 50)

    query += "LIMIT ?"
    params.append(limit)

    rows = execute_query(query, tuple(params))
    return {"count": len(rows), "tickets": rows}

#=========================================================================================================================

@mcp.tool
async def get_ticket_details(ticket_id: str) -> Dict[str, Any]:
    """Get full details of one support ticket."""

    query = """SELECT ticket_id, service_name, priority, status, subject, description, created_at, customer_impact, assigned_group
            FROM tickets WHERE ticket_id=?"""

    rows = execute_query(query, (ticket_id,))
    if not rows:
        return {"found": False, "message": "Ticket not found."}

    return {"found": True, "ticket": rows[0]}

#=========================================================================================================================

@mcp.tool
async def get_high_priority_tickets(service_name: str = None) -> Dict[str, Any]:
    """Return open P1 and P2 tickets. Optionally filter by service."""

    query ="""SELECT ticket_id, service_name, priority, status, subject 
        FROM tickets WHERE status='OPEN' AND priority IN ('P1','P2') """

    params: List[Any] = []
    if service_name:
        query += "AND service_name=? "
        params.append(service_name)

    query += "LIMIT 50"

    rows = execute_query(query, tuple(params))
    return {"count": len(rows), "tickets": rows}


if __name__=="__main__":
    mcp.run()
