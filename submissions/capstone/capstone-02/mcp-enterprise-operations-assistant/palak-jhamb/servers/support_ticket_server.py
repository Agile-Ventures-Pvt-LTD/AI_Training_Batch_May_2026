from fastmcp import FastMCP
import sqlite3
import os

DB_path=os.path.join(os.path.dirname(__file__),"..","data","tickets.db")
mcp = FastMCP("Support Ticket MCP Server")

@mcp.tool
def search_tickets(service_name: str = None,priority: str = None,status: str = None):
    """ Search support tickets using predefined filters such as service name, priority, status
    input optional arg:
    service_name: str
    priority: str
    status: str
    
    """
    query = "SELECT * FROM tickets WHERE 1=1"
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
    

    conn = sqlite3.connect(DB_path)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        tickets = []
        for ticket in rows:
            one_ticket = {
                "ticket_id": ticket["ticket_id"],
                "service_name": ticket["service_name"],
                "priority": ticket["priority"],
                "status": ticket["status"],
                "subject": ticket["subject"],
                "description": ticket["description"],
                "created_at": ticket["created_at"],
                "customer_impact": ticket["customer_impact"],
                "assigned_group": ticket["assigned_group"]
            }

            tickets.append(one_ticket)

        return {
            "count": len(tickets),
            "tickets": tickets
        }

    finally:
        conn.close()

    

       

@mcp.tool
def get_ticket_details(ticket_id: str = None)->dict:
    """Get full details of one support ticket"""
    query = None
    params = ()

    if ticket_id:
        query = "SELECT * FROM tickets WHERE ticket_id = ?"
        params = (ticket_id,)

    else:
        return {
            "found": False,
            "message": "Ticket not found."
        }

    conn = sqlite3.connect(DB_path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        ticket = cursor.fetchone()
        if not ticket:
            return {
                "found": False,
                "message": "Ticket not found."
            }
        return {
            "found": True,
            "ticket": {
                "ticket_id": ticket["ticket_id"],
                "service_name": ticket["service_name"],
                "priority": ticket["priority"],
                "status": ticket["status"],
                "subject": ticket["subject"],
                "description": ticket["description"],
                "created_at": ticket["created_at"],
                "customer_impact": ticket["customer_impact"],
                "assigned_group": ticket["assigned_group"]
            }
        }

    finally:
        conn.close()

@mcp.tool
def get_high_priority_tickets(service_name: str = None)->dict:
    """ get high priority tickets that can be filter by service_name as well"""
    query = "SELECT * FROM tickets WHERE priority IN ('P1', 'P2') AND status = 'OPEN'"
    params = []

    if service_name:
            query += " AND service_name = ?"
            params.append(service_name)


    conn = sqlite3.connect(DB_path)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        tickets = []
        for ticket in rows:
            one_ticket = {
                "ticket_id": ticket["ticket_id"],
                "service_name": ticket["service_name"],
                "priority": ticket["priority"],
                "status": ticket["status"],
                "subject": ticket["subject"],
                "description": ticket["description"],
                "created_at": ticket["created_at"],
                "customer_impact": ticket["customer_impact"],
                "assigned_group": ticket["assigned_group"]
            }

            tickets.append(one_ticket)

        return {
            "count": len(tickets),
            "tickets": tickets
        }

    finally:
        conn.close()



if __name__ == "__main__":
    mcp.run()


