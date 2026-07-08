import os
import json
import sqlite3
from typing import Optional, Any
from fastmcp import FastMCP

mcp = FastMCP("Support Ticket Server")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.db")

def run_query(sql: str, params: tuple = ()) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(sql, params).fetchall()]

def mapping(row: dict) -> dict:
    if isinstance(row, list):
        row = row[0]
    priority = {"High": "P1", "Medium": "P2", "Low": "P3"}
    return {"ticket_id": f"TKT-{row['ticket_id']}","service_name": row.get("service_name", ""),"priority": priority.get(row.get("priority"), "P3"),"status": str(row.get("status", "")).upper(),"subject": row.get("subject", ""),"description": row.get("description", ""),"created_at": row.get("created_at", ""),"customer_impact": row.get("customer_impact", ""),"assigned_group": row.get("assigned_group", "")}

@mcp.tool()
def search_tickets(service_name: Optional[Any] = None, priority: Optional[Any] = None, status: Optional[Any] = None, limit: int = 20) -> str:
    """This will search support tickets"""
    if isinstance(service_name, list) and service_name:
        service_name = service_name[0]
    if isinstance(priority, list) and priority:
        priority = priority[0]
    if isinstance(status, list) and status:
        status = status[0]

    sql = "SELECT * FROM operational_tickets WHERE 1=1"
    value = []
    
    if service_name and str(service_name).strip():
        srv_str = str(service_name).replace(" ", "-").lower()
        sql += " AND (LOWER(service_name) = ? OR LOWER(REPLACE(service_name, '_', '-')) = ?)"
        value.extend([srv_str, srv_str])
        
    if priority and str(priority).strip():
        service = str(priority).upper()
        priority_map = {"P1": "High", "P2": "Medium", "P3": "Low"}
        sql += " AND priority = ?"
        value.append(priority_map.get(service, priority))
        
    if status and str(status).strip():
        sql += " AND UPPER(status) = ?"
        value.append(str(status).upper())
        
    sql += " LIMIT ?"
    value.append(min(max(1, limit), 50))
    
    rows = run_query(sql, tuple(value))
    tickets = [mapping(r) for r in rows if isinstance(r, dict)]
    return json.dumps({"count": len(tickets), "tickets": tickets})

@mcp.tool()
def get_ticket_details(ticket_id: Any) -> str:
    """Get full details of one support ticket."""
    if isinstance(ticket_id, list) and ticket_id:
        ticket_id = ticket_id[0]
        
    clean_id = str(ticket_id).replace("TKT-", "").strip()
    rows = run_query("SELECT * FROM operational_tickets WHERE ticket_id = ?", (clean_id,))
    
    if not rows:
        return json.dumps({"found": False, "message": "Ticket is not found."})
        
    return json.dumps({"found": True, "ticket": mapping(rows[0])})

@mcp.tool()
def get_high_priority_tickets(service_name: Optional[Any] = None) -> str:
    """This will get high priority tickets and return open P1 and P2 tickets."""
    if isinstance(service_name, list) and service_name:
        service_name = service_name[0]

    sql = "SELECT * FROM operational_tickets WHERE priority IN ('High', 'Medium') AND UPPER(status) NOT IN ('CLOSED', 'RESOLVED')"
    value = []
    
    if service_name and str(service_name).strip():
        srv_str = str(service_name).replace(" ", "-").lower()
        sql += " AND (LOWER(service_name) = ? OR LOWER(REPLACE(service_name, '_', '-')) = ?)"
        value.extend([srv_str, srv_str])
        
    rows = run_query(sql, tuple(value))
    tickets = []
    
    for r in rows:
        if isinstance(r, dict):
            t = mapping(r)
            tickets.append({"ticket_id": t["ticket_id"],"service_name": t["service_name"],"priority": t["priority"],"status": t["status"],"subject": t["subject"]})
            
    return json.dumps({"count": len(tickets), "tickets": tickets})

if __name__ == "__main__":
    mcp.run()
