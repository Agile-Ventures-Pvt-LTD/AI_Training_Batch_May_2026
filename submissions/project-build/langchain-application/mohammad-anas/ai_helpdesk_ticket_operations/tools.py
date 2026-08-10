import json
from langchain_core.tools import tool
import db_utils

@tool
def search_tickets(status: str = None, priority: str = None):
    """Search for tickets based on status (Open, Closed) or priority (High, Low, etc)."""
    query = "SELECT ticket_id, customer_name, priority, status, subject, due_at FROM tickets WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
        
    query += " LIMIT 15"
    res = db_utils.read_db(query, tuple(params))
    return json.dumps(res)

@tool
def get_ticket_details(ticket_id: str):
    """Get full details of a specific ticket by its ID (e.g., TCK-00001)."""
    res = db_utils.read_db("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    return json.dumps(res)

@tool
def get_ticket_comments(ticket_id: str):
    """Fetch history, work notes, and comments for a specific ticket."""
    res = db_utils.read_db(
        "SELECT author, comment_type, comment, created_at FROM ticket_comments WHERE ticket_id = ? ORDER BY created_at ASC", 
        (ticket_id,)
    )
    return json.dumps(res)

@tool
def get_overdue_tickets():
    """Fetch a list of tickets that have breached SLA using the overdue_tickets view."""
    res = db_utils.read_db(
        "SELECT ticket_id, priority, status, subject, sla_status, due_at FROM overdue_tickets WHERE sla_status = 'BREACHED' LIMIT 10"
    )
    return json.dumps(res)

@tool
def prioritize_tickets():
    """Get the recommended ticket work queue ranked by priority score and SLA status."""
    res = db_utils.read_db(
        "SELECT ticket_id, priority, status, subject, sla_status, priority_score FROM ticket_work_queue ORDER BY priority_score DESC LIMIT 10"
    )
    return json.dumps(res)

@tool
def update_ticket_status(ticket_id: str, new_status: str):
    """Update the status of a ticket. Allowed: Open, In Progress, Pending Customer Response, Closed."""
    valid_statuses = ['Open', 'In Progress', 'Pending Customer Response', 'Closed']
    if new_status not in valid_statuses:
        return f"Error: '{new_status}' is not a valid status."

    existing = db_utils.read_db("SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,))
    if not existing or "error" in existing[0]:
        return "Ticket not found or DB error."

    q = "UPDATE tickets SET status = ? WHERE ticket_id = ?"
    res = db_utils.write_db(q, (new_status, ticket_id), "update_ticket_status", f"{ticket_id} -> {new_status}")
    
    if res.get("status") == "success":
        return f"Successfully updated {ticket_id} to {new_status}."
    return "Failed to update."

@tool
def add_ticket_comment(ticket_id: str, comment: str):
    """Add an internal note or comment to a ticket."""
    q = "INSERT INTO ticket_comments (ticket_id, author, comment_type, comment) VALUES (?, 'Agent', 'internal_note', ?)"
    res = db_utils.write_db(q, (ticket_id, comment), "add_ticket_comment", f"{ticket_id}: {comment}")
    
    if res.get("status") == "success":
        return "Comment added successfully."
    return "Failed to add comment."