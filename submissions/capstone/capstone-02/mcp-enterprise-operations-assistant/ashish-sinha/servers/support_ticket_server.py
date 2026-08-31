import sqlite3
from typing import Dict, List, Any, Optional
from fastmcp import FastMCP
from src.config import TICKET_DB_PATH

mcp = FastMCP("Support_Ticket_MCP_Server")

def connect_db(sql: str, params: tuple) -> List[Any]:
    connection = sqlite3.connect(TICKET_DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return rows

@mcp.tool
def search_tickets(
    service_name: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    result_limit = min(max(1, limit), 50)
    sql_query = "SELECT ticket_id, service_name, priority, status, subject, customer_impact, assigned_group FROM tickets WHERE 1=1"
    query_args = []
    if service_name:
        sql_query += " AND service_name = ?"
        query_args.append(service_name)
    if priority:
        sql_query += " AND priority = ?"
        query_args.append(priority)
    if status:
        sql_query += " AND status = ?"
        query_args.append(status)
    sql_query += " LIMIT ?"
    query_args.append(result_limit)
    records = connect_db(sql_query, tuple(query_args))
    return {"count": len(records), "tickets": records}

@mcp.tool
def get_ticket_details(ticket_id: str) -> Dict[str, Any]:
    sql_query = "SELECT * FROM tickets WHERE ticket_id = ?"
    records = connect_db(sql_query, (ticket_id,))
    if records:
        return {"found": True, "ticket": records[0]}
    return {"found": False, "message": "Ticket not found"}

@mcp.tool
def get_high_priority_tickets(service_name: Optional[str] = None) -> Dict[str, Any]:
    sql_query = "SELECT ticket_id, service_name, priority, status, subject FROM tickets WHERE status = 'OPEN' AND priority IN ('P1', 'P2')"
    query_args = []
    if service_name:
        sql_query += " AND service_name = ?"
        query_args.append(service_name)
    records = connect_db(sql_query, tuple(query_args))
    return {"count": len(records), "tickets": records}

if __name__ == "__main__":
    mcp.run()
