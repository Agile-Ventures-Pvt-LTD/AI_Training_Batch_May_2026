from datetime import datetime
from langchain.tools import tool

from db_utils import db
from config import (
    ALLOWED_STATUS,
    REFERENCE_TIME
)


def audit_log(
    tool_name,
    tool_input,
    tool_output,
    status="SUCCESS"
):
    """
    Save write operations into tool audit logs.
    """

    try:

        db.execute(
            """
            INSERT INTO tool_audit_logs
            (
                tool_name,
                input,
                output,
                status,
                created_at
            )
            VALUES
            (?, ?, ?, ?, ?)
            """,
            (
                tool_name,
                str(tool_input),
                str(tool_output),
                status,
                datetime.now().isoformat()
            )
        )

    except Exception:
        pass


def ticket_exists(ticket_id):
    """
    Validate ticket existence.
    """

    return db.exists(
        "tickets",
        "ticket_id",
        ticket_id
    )


@tool
def search_tickets(
    status=None,
    priority=None,
    category=None,
    assigned_agent=None,
    customer_tier=None,
    overdue_only=False,
    open_only=False,
    keyword=None
):
    """
    Search tickets using structured filters.
    """

    query = """
    SELECT *
    FROM ticket_work_queue
    WHERE 1=1
    """

    params = []

    filters = [
        ("status", status),
        ("priority", priority),
        ("category", category),
        ("assigned_agent", assigned_agent),
        ("customer_tier", customer_tier),
    ]

    for column, value in filters:

        if value:

            query += f" AND {column}=?"

            params.append(value)

    if overdue_only:

        query += """
        AND sla_state='BREACHED'
        """

    if open_only:

        query += """
        AND status!='Closed'
        """

    if keyword:

        query += """
        AND
        (
            subject LIKE ?
            OR description LIKE ?
        )
        """

        params.extend(
            [
                f"%{keyword}%",
                f"%{keyword}%"
            ]
        )

    rows = db.fetch_all(
        query,
        tuple(params)
    )

    return {
        "count": len(rows),
        "tickets": rows
    }


@tool
def get_ticket_details(
    ticket_id
):
    """
    Fetch complete details for a ticket.
    """

    return db.fetch_one(
        """
        SELECT
            t.*,
            c.customer_name,
            c.company_name,
            c.customer_tier
        FROM tickets t
        LEFT JOIN customers c
        ON t.customer_id=c.customer_id
        WHERE t.ticket_id=?
        """,
        (
            ticket_id,
        )
    )


@tool
def get_ticket_comments(
    ticket_id
):
    """
    Fetch comments and work history.
    """

    return db.fetch_all(
        """
        SELECT *
        FROM ticket_comments
        WHERE ticket_id=?
        ORDER BY created_at
        """,
        (
            ticket_id,
        )
    )


@tool
def calculate_sla_status(
    ticket_id
):
    """
    Determine SLA status.
    """

    row = db.fetch_one(
        """
        SELECT *
        FROM ticket_work_queue
        WHERE ticket_id=?
        """,
        (
            ticket_id,
        )
    )

    if not row:

        return {
            "error":
            "ticket not found"
        }

    return {

        "ticket_id":
        ticket_id,

        "sla_status":
        row["sla_state"],

        "due_at":
        row["due_at"],

        "status":
        row["status"],

        "reason":
        f"reference={REFERENCE_TIME}"
    }


@tool
def prioritize_tickets():
    """
    Rank tickets using priority and memory.
    """

    preferences = db.fetch_all(
        """
        SELECT *
        FROM archival_memory
        ORDER BY importance DESC
        LIMIT 5
        """
    )

    rows = db.fetch_all(
        """
        SELECT *
        FROM ticket_work_queue
        WHERE status!='Closed'
        ORDER BY priority_score DESC
        LIMIT 20
        """
    )

    return {
        "count": len(rows),
        "preferences": preferences,
        "tickets": rows
    }


@tool
def update_ticket_status(
    ticket_id,
    new_status
):
    """
    Update ticket status safely.
    """

    if not ticket_exists(ticket_id):

        return {
            "error":
            "ticket not found"
        }

    if new_status not in ALLOWED_STATUS:

        return {
            "error":
            "invalid status"
        }

    current = db.fetch_one(
        """
        SELECT status
        FROM tickets
        WHERE ticket_id=?
        """,
        (
            ticket_id,
        )
    )

    if current["status"] == new_status:

        return {
            "message":
            "already updated"
        }

    db.execute(
        """
        UPDATE tickets
        SET status=?
        WHERE ticket_id=?
        """,
        (
            new_status,
            ticket_id
        )
    )

    result = {
        "ticket_id": ticket_id,
        "old_status": current["status"],
        "new_status": new_status
    }

    audit_log(
        "update_ticket_status",
        ticket_id,
        result
    )

    return result


@tool
def add_ticket_comment(
    ticket_id,
    comment
):
    """
    Add internal comment.
    """

    if not ticket_exists(ticket_id):

        return {
            "error":
            "ticket not found"
        }

    db.execute(
        """
        INSERT INTO ticket_comments
        (
            ticket_id,
            comment
        )
        VALUES
        (?,?)
        """,
        (
            ticket_id,
            comment
        )
    )

    result = {
        "saved": True
    }

    audit_log(
        "add_ticket_comment",
        ticket_id,
        result
    )

    return result