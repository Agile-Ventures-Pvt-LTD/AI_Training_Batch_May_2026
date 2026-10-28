import os
import sqlite3
from fastmcp import FastMCP
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()
os.environ["DB_PATH"] = os.getenv("DB_PATH")

def get_connection():
    return sqlite3.connect(os.environ["DB_PATH"])


def execute_query(query: str, params=()):
    try:
        conn = get_connection()
        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conn.close()

        return [dict(row) for row in rows]
    except Exception as e:
        print(e)


mcp = FastMCP(name="support_ticket_server", instructions="This server will provide the information about the support tickets")


@mcp.tool(name="search_tickets", description="Search the support tickets using the predifined filters")
def search_tickets(
    service_name: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    limit: Optional[int] = 50
) -> Dict:
    """
    Search the support tickets using the predifined filters
    - service_name
    - priority
    - status
    - limit max_limit set to 50

    Args:
        service_name: name of the service
        priority: priority is defined between P1, P2, P3 and P4
        status: status of the ticket is OPEN / RESOLVED
        limit: number of result default set to 50

    Returns:
        dict: the count of tickets and the list of all the tickets
    """

    query = """
    SELECT ticket_id, service_name, priority, status, subject, customer_impact, assigned_group
    FROM tickets
    WHERE 1 = 1
    """
    
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

    query += " LIMIT ?"
    params.append(limit)

    tickets = execute_query(query, tuple(params))

    return {
        "count" : len(tickets),
        "tickets" : tickets
    }


@mcp.tool(name="get_ticket_details", description="Get the full details of one support ticket using the ticket_id")
def get_ticket_details(ticket_id: str) -> Dict:
    """
    Get the full details of one support ticket using the ticket_id

    Args:
        ticket_id: id of the ticket

    Returns: 
        dict: full detail of the ticket using the ticket_id
    """

    query = """
    SELECT * FROM tickets WHERE ticket_id = ?
    """ 

    params = []
    params.append(ticket_id.upper())

    ticket = execute_query(query, tuple(params))

    if ticket:
        return {
            "found" : True,
            "ticket": ticket
        }
    
    return {
        "found" : False,
        "message" : "Ticket not found."
    }


@mcp.tool(name="get_high_priority_tickets", description="Gives list of high priority support tickets which currently open and having the priority of P1 and P2 tickets")
def get_high_priority_tickets(service_name: Optional[str] = None) -> Dict:
    """
    Gives list of high priority support tickets which currently open and 
    having the priority of P1 and P2 tickets.

    Args: 
        service_name (optional) : name of the service which tickets you have to find

    Returns: 
        dict: the list of open and high priority tickects based P1 and P2 priority and if service_name is also give than filtered according to that also
    """

    query = """
    SELECT ticket_id, service_name, priority, status, subject
    FROM tickets
    WHERE (priority="P1" OR priority ="P2") AND status="OPEN"
    """

    params = []

    if service_name:
        query += " AND service_name = ?"
        params.append(service_name)

    tickets = execute_query(query, tuple(params))

    return {
        "count" : len(tickets),
        "tickets" : tickets
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")