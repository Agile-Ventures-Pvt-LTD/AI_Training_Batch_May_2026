import sqlite3
from pathlib import Path
from fastmcp import FastMCP


mcp=FastMCP("support_ticket")


def get_data():
    return Path(__file__).resolve().parent.parent / "data" / "tickets.db"


@mcp.tool
def search_tickets(service_name:str = "",priority: str= "",status:str ="",limit:int =10):
    """Search tickets using predefined filters, also adding a max limit"""
    try:
        max_limit=10
        query="SELECT ticket_id, service_name, priority, status, subject, customer_impact, assigned_group FROM tickets WHERE 1=1"
        par=[]
        if service_name:
            query+= " AND service_name=?"
            par.append(service_name)
        if priority:
            query+= " AND priority=?"
            par.append(priority)
        if status:
            query+= " AND status=?"
            par.append(status)
        query+= " Limit ?"
        par.append(max_limit)
        with sqlite3.connect(get_data()) as conn:
            conn.row_factory= sqlite3.Row
            cursor=conn.cursor()
            cursor.execute(query,par)
            rows=cursor.fetchall()
        tickets=[]
        for r in rows:
            tickets.append({
                "ticket_id": r["ticket_id"],
                "service_name":r["service_name"],
                "priority":r["priority"],
                "status":r["status"],
                "subject":r["subject"],
                "customer_impact":r["customer_impact"],
                "assigned_group":r["assigned_group"]

            })
        return {
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        return {"error" : str(e)}
    
    
@mcp.tool
def get_ticket_details(ticket_id:str=""):
    "Get full details of one support ticket, ticket id is required"
    if not ticket_id:
        return {
            "found" : False,
            "msg" : "Enter ticket id"
        }
    try:
        query="SELECT ticket_id, service_name, priority, status, subject, description, created_at, customer_impact, assigned_group FROM tickets WHERE ticket_id=?"
        with sqlite3.connect(get_data()) as conn:
            conn.row_factory= sqlite3.Row
            cursor=conn.cursor()
            cursor.execute(query,(ticket_id,))
            r=cursor.fetchone()
        if r:
            return {
                "found" : True,
                "ticket" : {
                "ticket_id": r["ticket_id"],
                "service_name":r["service_name"],
                "priority":r["priority"],
                "status":r["status"],
                "subject":r["subject"],
                "description":r["description"],
                "created_at" :r["created_at"],
                "customer_impact":r["customer_impact"],
                "assigned_group":r["assigned_group"]

                }
            }
    except Exception as e:
        return {"error" : str(e)}
    
@mcp.tool
def get_high_priority_tickets(service_name:str=""):
    """Get open P1 and P2 tickets"""
    try:
        query="SELECT ticket_id, service_name, priority, status, subject FROM tickets WHERE status='OPEN' AND priority IN ('P1','P2') "
        par=[]
        if service_name:
            query+= " AND service_name=?"
            par.append(service_name)
        with sqlite3.connect(get_data()) as conn:
            conn.row_factory= sqlite3.Row
            cursor=conn.cursor()
            cursor.execute(query,par)
            rows=cursor.fetchall()
        tickets=[]
        for r in rows:
            tickets.append({
                "ticket_id": r["ticket_id"],
                "service_name":r["service_name"],
                "priority":r["priority"],
                "status":r["status"],
                "subject":r["subject"]

            })
        return {
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        return {"error" : str(e)}
    

if __name__=="__main__":
    mcp.run()