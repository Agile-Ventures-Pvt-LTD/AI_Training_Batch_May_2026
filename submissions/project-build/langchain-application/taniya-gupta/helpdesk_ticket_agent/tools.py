from langchain_core.tools import tool
from db_utils import DB
from memory import Memory
import json

db=None
memory=None

def init_tools(db_instance: DB, memory_instance: Memory):
    global db, memory
    db=db_instance
    memory=memory_instance

from pydantic import BaseModel, Field

class SearchTicketsInput(BaseModel):
    status: str = Field(None, description="The status of the ticket.")
    priority: str = Field(None, description="The priority level")
    customer_tier: str = Field(None, description="The tier of the customer")
    category: str = Field(None, description="The ticket category.")
    limit: int = Field(3, description="The maximum number of results to return. MUST be an integer. Max allowed is 5.")

def truncate_ticket_fields(ticket, max_chars = 150):
    """Truncate long text fields to avoid hitting LLM context limits."""
    fields_to_truncate = ['description', 'resolution', 'subject']
    for field in fields_to_truncate:
        if field in ticket and isinstance(ticket[field], str) and len(ticket[field]) > max_chars:
            ticket[field] = ticket[field][:max_chars] + "..."
    return ticket

@tool(args_schema=SearchTicketsInput)
def search_tickets(status = None, priority = None, 
                   customer_tier = None, category = None, limit = 3):
    """Search tickets by various filters. Results are limited to 3 to save space."""
    filters = {
        "status": status,
        "priority": priority,
        "customer_tier": customer_tier,
        "category": category
    }
    results = db.search_tickets(filters, limit=limit)
    truncated_results = [truncate_ticket_fields(t, max_chars=100) for t in results]
    return json.dumps(truncated_results, indent=2)

@tool
def get_ticket_details(ticket_id):
    """Fetch complete details for a single ticket by its ID."""
    ticket = db.get_ticket_by_id(ticket_id)
    if not ticket:
        return f"Ticket {ticket_id} not found."
    return json.dumps(truncate_ticket_fields(ticket, max_chars=300), indent=2)

@tool
def get_ticket_comments(ticket_id):
    """Fetch the latest 2 comments and history for a specific ticket."""
    query = """SELECT * FROM ticket_comments WHERE ticket_id = ? ORDER BY created_at DESC LIMIT 2"""
    results = db.execute_query(query, (ticket_id,))
    truncated_results = []
    for comment in results:
        if 'comment' in comment and len(comment['comment']) > 150:
            comment['comment'] = comment['comment'][:150] + "..."
        truncated_results.append(comment)
    return json.dumps(truncated_results, indent=2)

@tool
def calculate_sla_status(ticket_id):
    """Determine the SLA status (BREACHED, DUE_TODAY, WITHIN_SLA) for a ticket."""
    query = """
    SELECT ticket_id, status, due_at,
    CASE
        WHEN status = 'Closed' THEN 'CLOSED'
        WHEN datetime(due_at) < datetime('2026-06-12 09:00:00') THEN 'BREACHED'
        WHEN date(due_at) = date('2026-06-12 09:00:00') THEN 'DUE_TODAY'
        ELSE 'WITHIN_SLA'
    END AS sla_status
    FROM tickets WHERE ticket_id = ?
    """
    results = db.execute_query(query, (ticket_id,))
    if not results:
        return f"Ticket {ticket_id} not found."
    return json.dumps(results[0], indent=2)

@tool
def get_overdue_tickets(limit = 3):
    """Fetch a list of tickets that have breached their SLA due date. Results limited to top 3 by default."""
    final_limit = min(int(limit), 5)
    query = f"SELECT * FROM overdue_tickets ORDER BY due_at ASC LIMIT {final_limit}"
    results = db.execute_query(query)
    truncated_results = [truncate_ticket_fields(t, max_chars=100) for t in results]
    return json.dumps(truncated_results, indent=2)

@tool
def prioritize_tickets(limit = 3):
    """Get a prioritized work queue of tickets. Limited to top 3 by default."""
    final_limit = min(int(limit), 5)
    query = f"SELECT * FROM ticket_work_queue ORDER BY priority_score DESC, due_at ASC LIMIT {final_limit}"
    results = db.execute_query(query)
    truncated_results = [truncate_ticket_fields(t, max_chars=100) for t in results]
    return json.dumps(truncated_results, indent=2)

@tool
def update_ticket_status(ticket_id, new_status):
    """Update the status of a ticket. Allowed: Open, In Progress, Pending, Resolved, Closed, Escalated."""
    allowed_statuses = ["Open", "In Progress", "Pending", "Resolved", "Closed", "Escalated"]
    if new_status not in allowed_statuses:
        return f"Error: Status '{new_status}' is not allowed. Choose from {allowed_statuses}."
    
    ticket = db.get_ticket_by_id(ticket_id)
    if not ticket:
        return f"Error: Ticket {ticket_id} not found."
    
    old_status = ticket['status']
    if old_status == new_status:
        return f"Ticket {ticket_id} is already in status '{new_status}'."
    
    query = "UPDATE tickets SET status = ?, last_updated_at = CURRENT_TIMESTAMP WHERE ticket_id = ?"
    db.execute_update(query, (new_status, ticket_id))
    
    # Audit log
    audit_query = "INSERT INTO tool_audit_logs (tool_name, tool_input, tool_output) VALUES (?, ?, ?)"
    db.execute_update(audit_query, ("update_ticket_status", f"{ticket_id} -> {new_status}", "SUCCESS"))
    
    return f"Successfully updated ticket {ticket_id} from '{old_status}' to '{new_status}'."

@tool
def add_ticket_comment(ticket_id, comment, author = "Agent"):
    """Add an internal comment or work note to a ticket."""
    ticket = db.get_ticket_by_id(ticket_id)
    if not ticket:
        return f"Error: Ticket {ticket_id} not found."
    
    query = "INSERT INTO ticket_comments (ticket_id, author, comment, created_at, comment_type) VALUES (?, ?, ?, CURRENT_TIMESTAMP, 'internal_note')"
    db.execute_update(query, (ticket_id, author, comment))
    
    # Audit log
    audit_query = "INSERT INTO tool_audit_logs (tool_name, tool_input, tool_output) VALUES (?, ?, ?)"
    db.execute_update(audit_query, ("add_ticket_comment", f"{ticket_id}: {comment}", "SUCCESS"))
    
    return f"Comment added to ticket {ticket_id}."

@tool
def save_archival_memory(key, value, importance = 3):
    """Store long-term user preferences or business rules."""
    memory.save_archival_memory(key, value, importance=importance)
    return f"Preference '{key}' saved to archival memory."

@tool
def recall_archival_memory(keyword):
    """Retrieve long-term preferences or rules using a keyword."""
    results = memory.recall_archival_memory(keyword)
    return json.dumps(results, indent=2)

@tool
def save_conversation(session_id, user_message, agent_response, tools_used):
    """
    Store the user-agent interaction in the conversation logs.
    
    Args:
        session_id: The unique session identifier.
        user_message: The message sent by the user.
        agent_response: The response generated by the agent.
        tools_used: A JSON string list of tools used in this turn.
    """
    try:
        tools_list = json.loads(tools_used)
    except:
        tools_list = [tools_used]
    memory.save_conversation(session_id, user_message, agent_response, tools_list)
    return "Conversation interaction logged successfully."

@tool
def recall_conversation(keyword):
    """Recall past conversations from conversation logs using a keyword."""
    results = memory.recall_conversation(keyword)
    return json.dumps(results, indent=2)

@tool
def summarize_conversation(session_id, summary_text, key_decisions, open_items):
    """Store a summary of the current conversation, including key decisions and open items."""
    memory.save_summary(session_id, summary_text, key_decisions, open_items)
    return f"Summary for session {session_id} saved successfully."
