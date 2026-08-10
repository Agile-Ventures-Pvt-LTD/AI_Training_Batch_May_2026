# Import required libraries
import os
import sqlite3
from typing import Any, Optional
from fastmcp import FastMCP
try:
    from confserver import get_conn
except ImportError:
    from .confserver import get_conn

mcp = FastMCP("Support Ticket MCP Server")





# Tool: search_tickets

@mcp.tool()
async def search_tickets(
    service_name: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    limit: Optional[str] = 20
    ) -> dict[str, Any] :
    """Search support tickets using predefined filters: service_name, priority, status, limit. Strictly, at least one filter is needed.

    Args:
        service_name (Optional[str], optional): Service name associated with the tickets. Defaults to None.
        priority (Optional[str], optional): priority to filter tickets. Defaults to None.
        status (Optional[str], optional): status to filter tickets. Defaults to None.
        limit (Optional[str], optional): limit to filter tickets. Defaults to 20.

    Returns:
        dict[str, Any]: Returns tickets and their information.
    """
    try:
        conn = get_conn()
        cursor = conn.cursor()
        
        query = """
            SELECT
                t.ticket_id,
                t.service_name,
                t.priority,
                t.status,
                t.subject,
                t.customer_impact,
                t.assigned_group
            FROM tickets t
            WHERE"""
        params = []
        
        if service_name:
            query += " t.service_name = ?"
            params.append(service_name, )
        if priority:
            query += " AND t.priority = ?"
            params.append(priority)
        if status:
            query += " AND t.status = ?"
            params.append(status)
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        
        tickets = []
        for row in rows:
            tickets.append({
                'ticket_id': row[0],
                'service_name': row[1],
                'priority': row[2],
                'status': row[3],
                'subject': row[4],
                'customer_impact': row[5],
                'assigned_group': row[6]
            })
        
        conn.close()
        
        return {
            'count': len(tickets),
            'tickets': tickets
        }
    except ValueError:
        return {'count': 0, 'message': "No values found."}
    except Exception as e:
        return {'count': 0, 'message': f"Error: {e}"}





# Tool: get_ticket_details

@mcp.tool()
async def get_ticket_details(ticket_id: str) -> dict[str, Any] :
    """Fetch full details of one support ticket.

    Args:
        ticket_id (str): ticket id of the target ticket.

    Returns:
        dict[str, Any]: Returns ticket or error message.
    """
    try:
        conn = get_conn()
        cursor = conn.cursor()
        
        row = list(cursor.execute("""SELECT * FROM tickets WHERE ticket_id = ?""", [ticket_id]).fetchone())
        
        ticket = {
            'ticket_id': row[0],
            'service_name': row[1],
            'priority': row[2],
            'status': row[3],
            'subject': row[4],
            'description': row[5],
            'created_at': row[6],
            'customer_impact': row[7],
            'assigned_group': row[8]
        }
        
        
        conn.close()
        
        return {
            'found': True,
            'ticket': ticket
        }
    except Exception:
        return {
            'found': False,
            'message': "Ticket not found."
        }






# Tool: get_high_priority_tickets

# @mcp.tool()
async def get_high_priority_tickets(service_name: str = None) -> dict[str, Any] :
    """Fetches open P1 and P2 tickets with optionally filtering by service..

    Args:
        service_name (str): Service name to be used as filter optionally. Default to None.

    Returns:
        dict[str, Any]: _description_
    """
    try:
        conn = get_conn()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            t.ticket_id,
            t.service_name,
            t.priority,
            t.status,
            t.subject
        FROM tickets t
        WHERE (t.priority = 'P1' OR t.priority = 'P2') AND t.status = 'OPEN'
        """
        params = []
        
        if service_name:
            query += " AND service_name = ?"
            params.append(service_name)
        
        rows = cursor.execute(query, params).fetchall()
        rows = [list(l) for l in rows]
        
        conn.close()
        
        tickets = []
        
        for row in rows:
            tickets.append({
                'ticket_id': row[0],
                'service_name': row[1],
                'priority': row[2],
                'status': row[3],
                'subject': row[4]
            })
        
        return {
            'count': len(tickets),
            'tickets': tickets
        }
    except Exception:
        return {
            'count': 0,
            'message': "No such tickets found."
        }
