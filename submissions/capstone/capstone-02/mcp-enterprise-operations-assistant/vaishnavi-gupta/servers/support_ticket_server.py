import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("Enterprise Operations Server")


@mcp.tool()
def list_services(
    
        service_name: str,
        status: str,
        limits: int
    
) -> dict:
    """
    Search support tickets using predefined filters.
    """
    
    api_key = os.getenv("GROQ_API_KEY")
    data_source = "data/tickets.db"
    

    return {
        "count": 4,
        "tickets": [
            {
                "ticket_id": data_source["ticket_id"],
                "service_name": data_source["service_name"],
                "priority": data_source["priority"],
                "status": data_source["status"],
                "subject": data_source["subject"],
                "customer_impact": data_source["customer_impact"],
                "assigned_group": data_source["assigned_group"]
            }
        ]
}

@mcp.tool()
def get_ticket_details(ticket_id: str) -> dict:
        
    """
    Get full details of one support ticket.
    """
     
    api_key = os.getenv("GROQ_API_KEY")
    data_source = "data/tickets.db"

    return{
        "found": True,
        "ticket": {
            "ticket_id": data_source["ticket_id"],
            "service_name": data_source["service_name"],
            "priority": data_source["priority"],
            "status": data_source["status"],
            "subject": data_source["subject"],
            "description": data_source["description"],
            "created_at": data_source["created_at"],
            "customer_impact": data_source["customer_impact"],
            "assigned_group": data_source["assigned_group"]
    },
            "found": False,
            "message": "Ticket not found."
}

@mcp.tool()
def get_high_priority_tickets(service_name: str) ->dict :

    """
    Return open P1 and P2 tickets.
    """
     
    api_key = os.getenv("GROQ_API_KEY")
    data_source = "data/tickets.db"

    return{
        "count": 3,
        "tickets": [
            {
                "ticket_id": data_source["ticket_id"],
                "service_name": data_source["service_name"],
                "priority": data_source["priority"],
                "status": data_source["status"],
                "subject": data_source["subject"]
            }

        ]
    }
       
    







