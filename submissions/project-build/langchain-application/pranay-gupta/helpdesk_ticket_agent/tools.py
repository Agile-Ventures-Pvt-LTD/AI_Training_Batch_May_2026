from datetime import datetime

from langchain_core.tools import tool

from db_utils import (execute_select_query,execute_single_record_query,execute_update_query)

from config import ALLOWED_STATUSES

from memory import (save_archival_memory,get_archival_memory,search_conversation_history,log_tool_usage)


@tool
def search_tickets(status: str = None,priority: str = None,assigned_to: str = None,customer_tier: str = None,limit: int = 20):
    """
    Search tickets using filters such as status,
    priority, assigned agent, and customer tier.
    """

    query = """
    SELECT *
    FROM tickets
    WHERE 1=1
    """

    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if priority:
        query += " AND priority = ?"
        params.append(priority)

    if assigned_to:
        query += " AND assigned_to = ?"
        params.append(assigned_to)

    if customer_tier:
        query += " AND customer_tier = ?"
        params.append(customer_tier)

    query += """
    ORDER BY last_updated_at DESC
    LIMIT ?
    """

    params.append(limit)

    return execute_select_query(query, tuple(params))


@tool
def get_ticket_details(ticket_id: str):
    """
    Retrieve complete details for a ticket.
    """

    query = """
    SELECT *
    FROM tickets
    WHERE ticket_id = ?
    """

    return execute_single_record_query(query,
        (ticket_id,)
    )

@tool
def get_ticket_comments(ticket_id: str):
    """
    Retrieve all comments associated with a ticket.
    """

    query = """
    SELECT *
    FROM ticket_comments
    WHERE ticket_id = ?
    ORDER BY created_at ASC
    """

    return execute_select_query(query,
        (ticket_id,)
    )


@tool
def calculate_sla_status(ticket_id: str):
    """
    Calculate SLA status for a ticket.
    """

    query = """
    SELECT *
    FROM tickets
    WHERE ticket_id = ?
    """

    ticket = execute_single_record_query(query,
        (ticket_id,)
    )

    if not ticket:
        return {
            "success": False,
            "message": "Ticket not found"
        }

    due_at = ticket.get("due_at")

    if not due_at:
        return {
            "ticket_id": ticket_id,
            "sla_status": "NO_SLA"
        }

    due_time = datetime.fromisoformat(due_at)

    now = datetime.now()

    if now > due_time:
        return {
            "ticket_id": ticket_id,
            "sla_status": "BREACHED"
        }

    remaining = due_time - now

    return {
        "ticket_id": ticket_id,
        "sla_status": "ACTIVE",
        "hours_remaining": round(
            remaining.total_seconds() / 3600,
            2
        )
    }


@tool
def prioritize_tickets(limit: int = 10):
    """
    Retrieve highest priority work queue.
    """

    query = """
    SELECT *
    FROM ticket_work_queue
    LIMIT ?
    """

    return execute_select_query(
        query,
        (limit,)
    )

@tool
def get_open_tickets():
    """
    Retrieve all open tickets.
    """

    query = """
    SELECT *
    FROM open_tickets
    """

    return execute_select_query(query)

@tool
def get_overdue_tickets():
    """
    Retrieve all overdue tickets.
    """

    query = """
    SELECT *
    FROM overdue_tickets
    """

    return execute_select_query(query)

@tool
def update_ticket_status(
    session_id: str,
    ticket_id: str,
    new_status: str
):
    """
    Update ticket status.
    """

    if new_status not in ALLOWED_STATUSES:

        return {
            "success": False,
            "message": f"Invalid status: {new_status}"
        }

    query = """
    UPDATE tickets
    SET
        status = ?,
        last_updated_at = ?
    WHERE ticket_id = ?
    """

    rows = execute_update_query(
        query,
        (
            new_status,
            datetime.now().isoformat(),
            ticket_id
        )
    )

    result = {
        "success": rows > 0,
        "ticket_id": ticket_id,
        "new_status": new_status
    }

    log_tool_usage(
        session_id=session_id,
        tool_name="update_ticket_status",
        tool_input=f"{ticket_id}->{new_status}",
        tool_output=str(result)
    )

    return result

@tool
def add_ticket_comment(
    session_id: str,
    ticket_id: str,
    author: str,
    comment: str,
    comment_type: str = "Internal Note"
):
    """
    Add comment to ticket.
    """

    query = """
    INSERT INTO ticket_comments
    (
        ticket_id,
        author,
        comment_type,
        comment,
        created_at
    )
    VALUES (?, ?, ?, ?, ?)
    """

    execute_update_query(
        query,
        (
            ticket_id,
            author,
            comment_type,
            comment,
            datetime.now().isoformat()
        )
    )

    result = {
        "success": True,
        "ticket_id": ticket_id,
        "comment_added": True
    }

    log_tool_usage(
        session_id=session_id,
        tool_name="add_ticket_comment",
        tool_input=comment,
        tool_output=str(result)
    )

    return result


@tool
def get_customer_history(customer_id: str):
    """
    Retrieve complete ticket history
    for a customer.
    """

    query = """
    SELECT *
    FROM tickets
    WHERE customer_id = ?
    ORDER BY created_at DESC
    """

    return execute_select_query(
        query,
        (customer_id,)
    )


@tool
def save_memory(
    memory_key: str,
    memory_value: str,
    importance: int = 3
):
    """
    Save information into archival memory.
    """

    save_archival_memory(
        memory_key=memory_key,
        memory_value=memory_value,
        memory_type="preference",
        importance=importance
    )

    return {
        "success": True,
        "memory_key": memory_key
    }


@tool
def recall_memory(memory_key: str):
    """
    Retrieve information from archival memory.
    """

    memory = get_archival_memory(
        memory_key
    )

    if not memory:
        return {
            "found": False
        }

    return {
        "found": True,
        "memory": memory
    }

@tool
def recall_conversation(keyword: str):
    """
    Search previous conversation history.
    """

    return search_conversation_history(
        keyword
    )