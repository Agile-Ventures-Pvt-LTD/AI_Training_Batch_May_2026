from langchain_core.tools import tool
from db_utils import execute_query
import sqlite3
from config import DB_PATH
from datetime import datetime

def audit_log(
    action,
    ticket_id
):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tool_audit_logs
        (
            tool_name,
            target_ticket_id
        )
        VALUES (?,?)
        """,
        (
            action,
            ticket_id
        )
    )

    conn.commit()
    conn.close()


#search ticket
@tool
def search_tickets(
    status=None,
    priority=None,
    category=None,
    assigned_to=None,
    customer_tier=None,
    overdue_only=False,
    keyword=None
    ):

    """
    Search tickets using filters.
    """

    query = """
    SELECT
        ticket_id,
        subject,
        priority,
        status,
        customer_tier,
        category,
        assigned_to,
        due_at
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

    if keyword:
        query += """
        AND (
            subject LIKE ?
            OR description LIKE ?
        )
        """
        params.extend([
            f"%{keyword}%",
            f"%{keyword}%"
        ])

    results = execute_query(
        query,
        tuple(params)
    )

    if overdue_only:

        from datetime import datetime

        reference_time = datetime(
            2026, 6, 12, 9, 0, 0
        )

        filtered = []

        for row in results:

            if row["due_at"]:

                due = datetime.fromisoformat(
                    row["due_at"]
                )

                if due < reference_time:
                    filtered.append(row)

        results = filtered

    return {
        "count": len(results),
        "tickets": results
    }

#calculate sla status
@tool
def calculate_sla_status(ticket_id: str):

    """
    Calculate SLA status for a ticket.
    """

    query = """
    SELECT due_at,status
    FROM tickets
    WHERE ticket_id=?
    """

    result = execute_query(query, (ticket_id,))

    if not result:
        return {"error": "Ticket not found"}

    due_date = datetime.fromisoformat(
        result[0]["due_at"]
    )

    today = datetime.now()

    if due_date.date() < today.date():
        sla = "BREACHED"

    elif due_date.date() == today.date():
        sla = "DUE_TODAY"

    else:
        sla = "WITHIN_SLA"

    return {
        "ticket_id": ticket_id,
        "sla_status": sla
    }

#prioritiza tickets
@tool
def prioritize_tickets():

    """
    Prioritize open tickets based on priority, customer tier and preferences.
    """

    memory = execute_query(
        """
        SELECT memory_value
        FROM archival_memory
        """
    )

    preference = ""

    if memory:
        preference = (
            memory[-1]["memory_value"]
            .lower()
        )

    tickets = execute_query(
        """
        SELECT *
        FROM open_tickets
        """
    )

    ranked = []

    for ticket in tickets:

        score = 0

        if ticket["priority"] == "Urgent":
            score += 50

        elif ticket["priority"] == "High":
            score += 25

        if ticket["customer_tier"] == "Enterprise":
            score += 30

        if (
            "enterprise"
            in preference
            and
            ticket["customer_tier"]
            ==
            "Enterprise"
        ):
            score += 100

        ranked.append({
            "ticket_id":
                ticket["ticket_id"],
            "subject":
                ticket["subject"],
            "score":
                score
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:10]

#update ticket status
@tool
def update_ticket_status(
    ticket_id: str,
    new_status: str
):
    """
    Update the status of a ticket.
    """
    valid_status = [
        "Open",
        "Closed",
        "Pending Customer Response",
        "In Progress"
    ]

    if new_status not in valid_status:

        return {
            "error": "Invalid status"
        }

    ticket = execute_query(
        """
        SELECT status
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    if not ticket:

        return {
            "error": "Ticket not found"
        }

    old_status = ticket[0]["status"]

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
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

    conn.commit()
    conn.close()

    audit_log(
        "update_ticket_status",
        ticket_id
    )

    return {
        "ticket_id": ticket_id,
        "before": old_status,
        "after": new_status
    }

#save conversation
@tool
def save_conversation(
    user_message,
    agent_response
):
    
    """
    save a conversation log
    """

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO conversation_logs
        (
            user_message,
            agent_response
        )
        VALUES (?,?)
        """,
        (user_message, agent_response)
    )

    conn.commit()
    conn.close()

    return {"saved": True}

#recall conversation
@tool
def recall_conversation(keyword: str):

    """
    recall previous conversation matching a keyword
    """

    query = """
    SELECT *
    FROM conversation_logs
    WHERE user_message LIKE ?
    """

    return execute_query(
        query,
        (f"%{keyword}%",)
    )

#save archival memory
@tool
def save_archival_memory(
    memory_key: str,
    memory_value: str
):
    
    """
    Save long-term user preference in archival memory.
    """

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO archival_memory
        (
            memory_key,
            memory_value,
            memory_type,
            importance
        )
        VALUES (?,?,?,?)
        """,
        (
            memory_key,
            memory_value,
            "preference",
            5
        )
    )

    conn.commit()
    conn.close()

    return {
        "saved": True
    }

#recall archival memory
@tool
def recall_archival_memory():
    """
    Retrieve stored archival memories.
    """

    query = """
    SELECT *
    FROM archival_memory
    ORDER BY importance DESC
    """

    return execute_query(query)

#summarize conversation
@tool
def summarize_conversation(
    session_id,
    summary,
    key_decisions,
    open_items
):
    
    """
    Store a conversation summary.
    """

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO conversation_summaries
        (
            session_id,
            summary,
            key_decisions,
            open_items
        )
        VALUES (?,?,?,?)
        """,
        (
            session_id,
            summary,
            key_decisions,
            open_items
        )
    )

    conn.commit()
    conn.close()

    return {
        "stored": True
    }   

#get ticket details
@tool
def get_ticket_details(ticket_id: str):
    
    """
    Get complete details for a ticket.
    """

    query = """
    SELECT *
    FROM tickets
    WHERE ticket_id=?
    """

    result = execute_query(
        query,
        (ticket_id,)
    )

    if not result:

        return {
            "error":
            "Ticket not found"
        }

    return result[0]

#get ticket comments
@tool
def get_ticket_comments(
    ticket_id: str
):
    """
    Get all comments for a ticket.
    """

    query = """
    SELECT
        author,
        comment_type,
        comment,
        created_at
    FROM ticket_comments
    WHERE ticket_id=?
    ORDER BY created_at
    """

    return execute_query(
        query,
        (ticket_id,)
    )

#tickrt comment
@tool
def add_ticket_comment(
    ticket_id: str,
    comment: str
):
    """
    Add an internal comment to a ticket.
    """

    # 1. Validate ticket exists

    ticket = execute_query(
        """
        SELECT ticket_id, subject
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    if not ticket:

        return {
            "success": False,
            "message": f"Ticket {ticket_id} not found"
        }

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    try:

        # 2. Add comment

        cur.execute(
            """
            INSERT INTO ticket_comments
            (
                ticket_id,
                author,
                comment_type,
                comment,
                created_at
            )
            VALUES (?,?,?,?,datetime('now'))
            """,
            (
                ticket_id,
                "AI Helpdesk Agent",
                "Internal",
                comment
            )
        )

        # 3. Audit Log

        cur.execute(
            """
            INSERT INTO tool_audit_logs
            (
                tool_name,
                target_ticket_id,
                action_details,
                created_at
            )
            VALUES (?,?,?,datetime('now'))
            """,
            (
                "add_ticket_comment",
                ticket_id,
                f"Added comment: {comment}"
            )
        )

        conn.commit()

        return {
            "success": True,
            "ticket_id": ticket_id,
            "subject": ticket[0]["subject"],
            "comment_added": comment,
            "message": "Comment added successfully"
        }

    except Exception as e:

        conn.rollback()

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        conn.close()