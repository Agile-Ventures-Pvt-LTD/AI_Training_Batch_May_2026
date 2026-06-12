import db_utils

try:
    from langchain.tools import tool
except ImportError:
    from langchain_core.tools import tool


@tool
def ticket_status_counts():
    """Show how many tickets are in each status."""
    return db_utils.count_tickets_by_status()


@tool
def search_tickets(keyword=None, status=None, priority=None, limit=10):
    """Search tickets by keyword, status, or priority."""
    rows = db_utils.search_tickets(
        keyword=keyword,
        status=status,
        priority=priority,
        limit=limit,
    )

    tickets = []
    for row in rows:
        tickets.append(
            {
                "ticket_id": row["ticket_id"],
                "subject": row["subject"],
                "priority": row["priority"],
                "status": row["status"],
                "customer": row["customer_name"],
                "due_at": row["due_at"],
            }
        )

    return {"count": len(tickets), "tickets": tickets}


@tool
def get_ticket_details(ticket_id):
    """Get all details for one ticket."""
    return db_utils.get_ticket_details(ticket_id)


@tool
def get_ticket_comments(ticket_id):
    """Get comments for one ticket."""
    return db_utils.get_ticket_comments(ticket_id)


@tool
def get_overdue_tickets(limit=10):
    """Get overdue tickets."""
    return db_utils.get_overdue_tickets(limit)


@tool
def get_work_queue(limit=10):
    """Get the highest priority open tickets."""
    return db_utils.get_work_queue(limit)


@tool
def update_ticket_status(ticket_id, status):
    """Update a ticket status."""
    return db_utils.update_ticket_status(ticket_id, status)


TOOLS = [
    ticket_status_counts,
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    get_overdue_tickets,
    get_work_queue,
    update_ticket_status,
]
