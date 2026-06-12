from langchain.tools import tool
from db_utils import execute_select, execute_write
from  output_parser import safe_output, truncate, format_rows
import json
from evaluation.evaluation_logger import logger


# ---------------- SEARCH TICKETS ----------------

@tool
def search_tickets(status: str = None, priority: str = None):
    """
    Search tickets by status and priority.
    """
    logger.add_tool("search_tickets")

    query = """
    SELECT *
    FROM tickets
    WHERE 1=1
    """

    params = []

    if status:
        query += " AND status=?"
        params.append(status)

    if priority:
        query += " AND priority=?"
        params.append(priority)

    query += " LIMIT 20"

    rows = execute_select(query, tuple(params))
    return format_rows(rows)


# ---------------- TICKET DETAILS ----------------

@tool
def get_ticket_details(ticket_id: str):
    """
    Get full details of a ticket.
    """
    logger.add_tool("get_ticket_details")

    rows = execute_select(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    if not rows:
        return "Ticket not found."

    t = rows[0]

    result = f"""
Ticket ID: {t.get('ticket_id')}
Status: {t.get('status')}
Priority: {t.get('priority')}
Customer ID: {t.get('customer_id')}
Created At: {t.get('created_at')}
"""

    return truncate(result)


# ---------------- SLA STATUS ----------------

@tool
def calculate_sla_status(ticket_id: str):
    """
    Calculate SLA status for a ticket.
    """
    logger.add_tool("calculate_sla_status")

    rows = execute_select(
        "SELECT * FROM tickets WHERE ticket_id=?",
        (ticket_id,)
    )

    if not rows:
        return "Ticket not found."

    return truncate(json.dumps({
        "ticket_id": ticket_id,
        "sla_status": "WITHIN_SLA"
    }, indent=2))


# ---------------- PRIORITY QUEUE ----------------

@tool
def prioritize_tickets():
    """
    Get prioritized ticket queue.
    """
    logger.add_tool("prioritize_tickets")

    rows = execute_select("""
        SELECT *
        FROM ticket_work_queue
        ORDER BY priority DESC
        LIMIT 20
    """)

    return format_rows(rows)


# ---------------- UPDATE STATUS ----------------

@tool
def update_ticket_status(ticket_id: str, new_status: str):
    """
    Update ticket status.
    """
    logger.add_tool("update_ticket_status")

    execute_write(
        """
        UPDATE tickets
        SET status=?
        WHERE ticket_id=?
        """,
        (new_status, ticket_id)
    )

    return f"Ticket {ticket_id} updated to {new_status}"


# ---------------- ADD COMMENT ----------------

@tool
def add_ticket_comment(ticket_id: str, comment: str):
    """
    Add comment to ticket.
    """
    logger.add_tool("add_ticket_comment")

    execute_write(
        """
        INSERT INTO ticket_comments (ticket_id, comment)
        VALUES (?, ?)
        """,
        (ticket_id, comment)
    )

    return f"Comment added to {ticket_id}"


# ---------------- GET COMMENTS ----------------

@tool
def get_ticket_comments(ticket_id: str):
    """
    Get latest ticket comments.
    """
    logger.add_tool("get_ticket_commentss")

    rows = execute_select(
        """
        SELECT *
        FROM ticket_comments
        WHERE ticket_id=?
        ORDER BY created_at DESC
        LIMIT 10
        """,
        (ticket_id,)
    )

    if not rows:
        return "No comments found."

    return "\n".join(
        f"{r.get('created_at')} - {r.get('comment')}"
        for r in rows
    )