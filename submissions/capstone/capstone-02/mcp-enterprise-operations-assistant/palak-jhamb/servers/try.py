import os
import sqlite3

DB_path=os.path.join(os.path.dirname(__file__),"..","data","tickets.db")

def search_tickets(service_name: str = None,priority: str = None,status: str = None):
    """ Search support tickets using predefined filters such as service name, priority, status"""
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
    


data=search_tickets(service_name = "Payment API")
print(data)