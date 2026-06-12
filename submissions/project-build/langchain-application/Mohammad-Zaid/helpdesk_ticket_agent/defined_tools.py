# defined_tools.py (tools.py)
from langchain.tools import tool

from db_utils import run_query

"""
search_tickets
get_ticket_details
get_ticket_comments
prioritize_tickets
update_ticket_status
add_ticket_comment
"""


# Search tickets tool

@tool
def search_tickets(query: str):
    """
    Search tickets.
    Examples:
    open tickets
    high priority tickets
    overdue tickets
    """

    query = query.lower()

    if "overdue" in query:

        sql = """
        SELECT ticket_id, customer_name, priority, status, sla_status
        FROM overdue_tickets
        LIMIT 10
        """

    elif "high" in query:

        sql = """
        SELECT ticket_id, customer_name, priority, status
        FROM tickets
        WHERE priority='High'
        LIMIT 10
        """

    elif "open" in query:

        sql = """
        SELECT ticket_id, customer_name, priority, status
        FROM open_tickets
        LIMIT 10
        """

    else:

        sql = """
        SELECT ticket_id, customer_name, priority, status
        FROM tickets
        LIMIT 10
        """
    return str(run_query(sql))

# Get ticket details

@tool
def get_ticket_details(ticket_id: str):
    """
    Get complete ticket details.
    Example:
    TCK-00077
    """

    result = run_query(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )
    return str(result)

# Get ticket comments

@tool
def get_ticket_comments(ticket_id: str):
    """
    Get ticket comments and history.
    """

    result = run_query(
        """
        SELECT author, comment_type, comment, created_at
        FROM ticket_comments
        WHERE ticket_id = ?
        ORDER BY created_at
        """,
        (ticket_id,)
    )
    return str(result)

# Prioritize tickets

@tool
def prioritize_tickets(dummy: str = ""):
    """
    Use this tool when the user asks:
    - which tickets should I work on first
    - ticket priority
    - work queue
    - recommended tickets
    """

    result = run_query(
        """
        SELECT ticket_id, customer_name, priority, customer_tier, sla_status, priority_score
        FROM ticket_work_queue
        ORDER BY priority_score DESC
        LIMIT 10
        """
    )
    return str(result)

# Update ticket status

@tool
def update_ticket_status(ticket_id: str, new_status: str):
    """
    Update ticket status.
    """

    valid_statuses = ["Open", "In Progress", "Pending", "Resolved", "Closed", "Escalated"]

    if new_status not in valid_statuses:
        return "Invalid Status"

    result = run_query(
        """
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
        """,
        (new_status, ticket_id)
    )
    return f"{ticket_id} updated to {new_status}"

# Add internal ticket comment

@tool
def add_ticket_comment(ticket_id: str, comment: str):
    """
    Add ticket comment.
    """

    run_query(
        """
        INSERT INTO ticket_comments
        (ticket_id, author, comment_type, comment, created_at)
        VALUES
        (?, 'AI Agent', 'Internal Note', ?, CURRENT_TIMESTAMP)
        """,
        (ticket_id, comment)
    )
    return "Comment Successfully Added"

