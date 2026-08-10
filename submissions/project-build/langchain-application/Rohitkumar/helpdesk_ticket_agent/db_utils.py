import sqlite3
from datetime import datetime
from config import DB_PATH


# DATABASE CONNECTION

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def validate_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = [row["name"] for row in cursor.fetchall()]

    conn.close()

    return tables



# TICKET SEARCH


def search_tickets_db(
    status=None,
    priority=None,
    category=None,
    assigned_to=None,
    customer_tier=None,
    keyword=None,
    overdue_only=False
):

    conn = get_connection()

    query = """
    SELECT *
    FROM ticket_work_queue
    WHERE 1=1
    """

    params = []

    if status:
        query += " AND LOWER(status)=LOWER(?)"
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
            OR category LIKE ?
            OR assigned_to LIKE ?
        )
        """

        params.extend([
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ])

    if overdue_only:
        query += """
        AND sla_status='BREACHED'
        """

    cursor = conn.cursor()

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# TICKET DETAILS


def get_ticket_details_db(ticket_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return dict(row)



# TICKET COMMENTS


def get_ticket_comments_db(ticket_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM ticket_comments
        WHERE ticket_id=?
        ORDER BY created_at
        """,
        (ticket_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# OVERDUE TICKETS


def get_overdue_tickets_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM overdue_tickets
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# WORK QUEUE


def get_ticket_work_queue_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM ticket_work_queue
        ORDER BY priority_score DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# SLA STATUS


def calculate_sla_status_db(ticket_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ticket_id,
            due_at,
            status,
            sla_status
        FROM ticket_work_queue
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return dict(row)



# UPDATE STATUS


def update_ticket_status_db(
        ticket_id,
        new_status
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    row = cursor.fetchone()

    if not row:

        conn.close()

        return {
            "success": False,
            "message": "Ticket not found"
        }

    current_status = row["status"]

    if current_status == new_status:

        conn.close()

        return {
            "success": False,
            "message": "Ticket already in requested status"
        }

    cursor.execute(
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

    return {
        "success": True,
        "ticket_id": ticket_id,
        "old_status": current_status,
        "new_status": new_status
    }


# ADD COMMENT


def add_comment_db(
        ticket_id,
        comment,
        author="AI Agent"
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ticket_comments(
            ticket_id,
            author,
            comment_type,
            comment,
            created_at
        )
        VALUES(?,?,?,?,?)
        """,
        (
            ticket_id,
            author,
            "Internal",
            comment,
            datetime.now().isoformat()
        )
    )

    conn.commit()

    conn.close()

    return {
        "success": True,
        "ticket_id": ticket_id
    }


# CONVERSATION LOGS


def save_conversation_db(
        session_id,
        user_message,
        agent_response,
        tools_used
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversation_logs(
            session_id,
            user_message,
            agent_response,
            tools_used,
            created_at
        )
        VALUES(?,?,?,?,?)
        """,
        (
            session_id,
            user_message,
            agent_response,
            str(tools_used),
            datetime.now().isoformat()
        )
    )

    conn.commit()

    conn.close()


def recall_conversation_db(keyword):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM conversation_logs
        WHERE user_message LIKE ?
           OR agent_response LIKE ?
        ORDER BY created_at DESC
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# ARCHIVAL MEMORY


def save_archival_memory_db(
        memory_key,
        memory_value,
        memory_type="preference",
        importance=5
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO archival_memory(
            memory_key,
            memory_value,
            memory_type,
            importance,
            created_at
        )
        VALUES(?,?,?,?,?)
        """,
        (
            memory_key,
            memory_value,
            memory_type,
            importance,
            datetime.now().isoformat()
        )
    )

    conn.commit()

    conn.close()


def recall_archival_memory_db(keyword):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM archival_memory
        WHERE memory_key LIKE ?
           OR memory_value LIKE ?
        ORDER BY importance DESC
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



# CONVERSATION SUMMARY


def save_conversation_summary_db(
        session_id,
        summary,
        key_decisions,
        open_items
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversation_summaries(
            session_id,
            summary,
            key_decisions,
            open_items,
            created_at
        )
        VALUES(?,?,?,?,?)
        """,
        (
            session_id,
            summary,
            key_decisions,
            open_items,
            datetime.now().isoformat()
        )
    )

    conn.commit()

    conn.close()



# AUDIT LOG
=

def audit_log_db(
        tool_name,
        tool_input,
        tool_output,
        status="SUCCESS"
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tool_audit_logs(
            tool_name,
            tool_input,
            tool_output,
            status,
            created_at
        )
        VALUES(?,?,?,?,?)
        """,
        (
            tool_name,
            str(tool_input),
            str(tool_output),
            status,
            datetime.now().isoformat()
        )
    )

    conn.commit()

    conn.close()