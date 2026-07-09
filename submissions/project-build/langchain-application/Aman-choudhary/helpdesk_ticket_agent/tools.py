from langchain.tools import tool
from db_utils import execute_query, execute_update


@tool
def search_tickets(status: str):
    """Search tickets by status."""

    query = """
    SELECT *
    FROM tickets
    WHERE status LIKE ?
    LIMIT 20
    """

    return execute_query(
        query,
        (f"%{status}%",)
    )


@tool
def get_ticket_details(ticket_id: str):
    """Get ticket details."""

    query = """
    SELECT *
    FROM tickets
    WHERE ticket_id = ?
    """

    return execute_query(
        query,
        (ticket_id,)
    )


@tool
def get_ticket_comments(ticket_id: str):
    """Get ticket comments."""

    query = """
    SELECT *
    FROM ticket_comments
    WHERE ticket_id = ?
    """

    return execute_query(
        query,
        (ticket_id,)
    )


@tool
def get_overdue_tickets(dummy: str):
    """Get overdue tickets."""

    query = """
    SELECT *
    FROM overdue_tickets
    """

    return execute_query(query)


@tool
def get_work_queue(dummy: str):
    """Get work queue."""

    query = """
    SELECT *
    FROM ticket_work_queue
    LIMIT 20
    """

    return execute_query(query)


@tool
def update_ticket_status(input_text: str):
    """
    Update ticket status.

    Example:
    TCK-1001,In Progress
    """

    try:

        ticket_id, new_status = input_text.split(",")

        query = """
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
        """

        execute_update(
            query,
            (
                new_status.strip(),
                ticket_id.strip()
            )
        )

        return f"{ticket_id} updated to {new_status}"

    except Exception as e:
        return str(e)


@tool
def save_archival_memory(text: str):
    """Save user preference."""

    query = """
    INSERT INTO archival_memory
    (
        memory_key,
        memory_value,
        memory_type,
        importance
    )
    VALUES
    (?, ?, ?, ?)
    """

    execute_update(
        query,
        (
            "user_preference",
            text,
            "preference",
            5
        )
    )

    return "Memory Saved"


@tool
def recall_archival_memory(dummy: str):
    """Recall saved memory."""

    query = """
    SELECT *
    FROM archival_memory
    ORDER BY rowid DESC
    LIMIT 10
    """

    return execute_query(query)