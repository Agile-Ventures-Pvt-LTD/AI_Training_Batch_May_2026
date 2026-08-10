from langchain.tools import tool
from database.connection import get_connection

@tool
def get_ticket_details(ticket_id):
    """
    Fetches ticket details for a given ticket_id
    """
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result


@tool
def get_overdue_tickets():
    """
    Fetches all overdue tickets.
    """
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM overdue_tickets
        LIMIT 20
        """
    )

    result = cursor.fetchall()

    conn.close()

    return result

@tool
def get_ticket_comments(ticket_id):
    """
    Fetches the comment of a specific ticket_id.
    """
    
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            author,
            comment_type,
            comment,
            created_at
        FROM ticket_comments
        WHERE ticket_id = ?
        ORDER BY created_at
        """,
        (ticket_id,)
    )

    result = cursor.fetchall()

    conn.close()

    return result



@tool
def get_work_queue():
    """
    Fetches the work queues ordered by priority.
    """
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM ticket_work_queue
        ORDER BY priority_score DESC
        LIMIT 20
        """
    )

    result = cursor.fetchall()

    conn.close()

    return result




@tool
def update_ticket_status(
    ticket_id: str,
    new_status: str
):
    """
    Update the status of an existing helpdesk ticket.
    """

    ALLOWED_STATUSES = {
        "Open",
        "Pending Customer Response",
        "Closed"
    }

    if new_status not in ALLOWED_STATUSES:
        return {
            "status": "error",
            "message": f"Invalid status: {new_status}"
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()

        return {
            "status": "error",
            "message": f"Ticket {ticket_id} not found"
        }

    old_status = row[0]

    cursor.execute(
        """
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
        """,
        (
            new_status,
            ticket_id
        )
    )

    conn.commit()

    conn.close()

    return {
        "status": "success",
        "ticket_id": ticket_id,
        "old_status": old_status,
        "new_status": new_status
    }
    


@tool
def add_ticket_comment(
    ticket_id: str,
    comment: str,
    author: str = "AI Agent",
    comment_type: str = "internal_note"
):
    """
    Add a comment to a helpdesk ticket.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ticket_id
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )

    if cursor.fetchone() is None:
        conn.close()

        return {
            "status": "error",
            "message": f"Ticket {ticket_id} not found"
        }

    cursor.execute(
        """
        INSERT INTO ticket_comments
        (
            ticket_id,
            author,
            comment_type,
            comment
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            ticket_id,
            author,
            comment_type,
            comment
        )
    )

    conn.commit()

    comment_id = cursor.lastrowid

    conn.close()

    return {
        "status": "success",
        "comment_id": comment_id,
        "ticket_id": ticket_id
    }
