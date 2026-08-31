import json
from langchain.tools import tool
from db_utils import run_select_query, run_write_query
from memory import (
    save_conversation_db,
    recall_conversation_db,
    save_archival_memory_db,
    recall_archival_memory_db,
    save_summary_db
)

ALLOWED_STATUSES = [
    "Open",
    "In Progress",
    "Closed",
]


def tool_response(data):
    return json.dumps(data, indent=2, default=str)


@tool
def search_tickets(
    status: str = "",
    priority: str = "",
    category: str = "",
    assigned_to: str = "",
    customer_tier: str = ""
):
    """
    Search helpdesk tickets when user provided the status, priority, category, assigned_to and customer_tier.
    """

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

    if category:
        query += " AND category=?"
        params.append(category)

    if assigned_to:
        query += " AND assigned_to=?"
        params.append(assigned_to)

    if customer_tier:
        query += " AND customer_tier=?"
        params.append(customer_tier)

    result = run_select_query(query, tuple(params))
    return tool_response(result)


@tool
def get_ticket_details(ticket_id: str):
    """
    Retrieve complete details for a specific ticket.
    """

    result = run_select_query(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    if not result:
        return tool_response(
            {"error": "Ticket not found"}
        )

    return tool_response(result[0])


@tool
def get_ticket_comments(ticket_id: str):
    """
    Retrieve comments, notes, and activity history for a ticket.
    """

    result = run_select_query(
        """
        SELECT
            comment_id,
            author,
            comment_type,
            comment,
            created_at
        FROM ticket_comments
        WHERE ticket_id=?
        ORDER BY created_at ASC
        """,
        (ticket_id,)
    )

    return tool_response(result)


@tool
def get_overdue_tickets():
    """
    Retrieve all overdue tickets.
    """

    result = run_select_query(
        """
        SELECT *
        FROM overdue_tickets
        ORDER BY due_at ASC
        """
    )

    return tool_response(result)


@tool
def prioritize_tickets():
    """
    Retrieve all the highest priority tickets that should be handled first.
    Tickets with the urgent tags
    """

    result = run_select_query(
        """
        SELECT *
        FROM ticket_work_queue
        ORDER BY priority_score DESC,
                 due_at ASC
        LIMIT 20
        """
    )

    return tool_response(result)


@tool
def update_ticket_status(
    ticket_id: str,
    new_status: str
):
    """
    Update the status of an existing ticket.
    Use when the user explicitly asks to change a ticket status.
    """

    if new_status not in ALLOWED_STATUSES:
        return tool_response({
            "success": False,
            "message": "Invalid status"
        })

    existing = run_select_query(
        """
        SELECT status
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    if not existing:
        return tool_response({
            "success": False,
            "message": "Ticket not found"
        })

    current_status = existing[0]["status"]

    if current_status == new_status:
        return tool_response({
            "success": False,
            "message": "Ticket already in requested status"
        })

    run_write_query(
        """
        UPDATE tickets
        SET
            status=?,
            last_updated_at=CURRENT_TIMESTAMP
        WHERE ticket_id=?
        """,
        (
            new_status,
            ticket_id
        )
    )

    return tool_response({
        "success": True,
        "ticket_id": ticket_id,
        "old_status": current_status,
        "new_status": new_status
    })


@tool
def add_ticket_comment(
    ticket_id: str,
    comment: str
):
    """
    Add an internal note or comment to a ticket.
    Use when the user wants to add information, notes, updates, or comments.
    """

    exists = run_select_query(
        """
        SELECT ticket_id
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    if not exists:
        return tool_response({
            "success": False,
            "message": "Ticket not found"
        })

    run_write_query(
        """
        INSERT INTO ticket_comments
        (
            ticket_id,
            author,
            comment_type,
            comment,
            created_at
        )
        VALUES
        (
            ?, ?, ?, ?, CURRENT_TIMESTAMP
        )
        """,
        (
            ticket_id,
            "Helpdesk Agent",
            "internal_note",
            comment
        )
    )

    return tool_response({
        "success": True,
        "message": "Comment added"
    })


@tool
def save_conversation(
    session_id: str,
    user_message: str,
    agent_response: str,
    tools_used: str = ""
):
    """
    Save a conversation to conversation history.
    """

    return save_conversation_db(
        session_id,
        user_message,
        agent_response,
        tools_used
    )


@tool
def recall_conversation(keyword: str):
    """
    Search previously saved conversations.
    """

    results = recall_conversation_db(keyword)

    if not results:
        return "No conversations found."

    return json.dumps(results, indent=2, default=str)


@tool
def save_archival_memory(
    memory_key: str,
    memory_value: str,
    memory_type: str = "preference",
    importance: int = 5
):
    """
    Save a long term user preference or memory.
    """

    return save_archival_memory_db(
        memory_key,
        memory_value,
        memory_type,
        importance
    )


@tool
def recall_archival_memory(keyword: str):
    """
    Search previously saved long term memories.
    """

    results = recall_archival_memory_db(keyword)

    if not results:
        return "No memories found."

    return json.dumps(results, indent=2, default=str)


@tool
def summarize_conversation(
    session_id: str,
    summary: str,
    key_decisions: str = "",
    open_items: str = ""
):
    """
    Store a summary of a completed conversation.
    Use when a conversation should be remembered for future reference.
    """

    return save_summary_db(
        session_id,
        summary,
        key_decisions,
        open_items
    )

tools = [
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    get_overdue_tickets,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
    save_conversation,
    recall_conversation,
    save_archival_memory,
    recall_archival_memory,
    summarize_conversation,
]
