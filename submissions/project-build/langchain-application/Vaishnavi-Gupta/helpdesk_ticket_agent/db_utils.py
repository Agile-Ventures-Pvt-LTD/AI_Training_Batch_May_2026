import sqlite3
from contextlib import contextmanager
from typing import Dict, List, Any, Optional

from config import DB_PATH


@contextmanager
def get_connection():
    """
    Context-managed SQLite connection.
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()


def fetch_all(
    query: str,
    params: tuple = ()
) -> List[Dict[str, Any]]:
    """
    Execute SELECT query and return rows.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(query, params)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]


def fetch_one(
    query: str,
    params: tuple = ()
) -> Optional[Dict[str, Any]]:
    """
    Execute SELECT query returning one row.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(query, params)

        row = cursor.fetchone()

        return dict(row) if row else None


def execute_write(
    query: str,
    params: tuple = ()
) -> int:
    """
    Execute INSERT/UPDATE.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

        return cursor.rowcount


def ticket_exists(ticket_id: str) -> bool:

    query = """
    SELECT ticket_id
    FROM tickets
    WHERE ticket_id = ?
    """

    result = fetch_one(query, (ticket_id,))

    return result is not None


def get_ticket_by_id(ticket_id: str):

    query = """
    SELECT *
    FROM tickets
    WHERE ticket_id = ?
    """

    return fetch_one(query, (ticket_id,))


def get_ticket_comments(ticket_id: str):

    query = """
    SELECT *
    FROM ticket_comments
    WHERE ticket_id = ?
    ORDER BY created_at ASC
    """

    return fetch_all(query, (ticket_id,))


def search_tickets_db(
    status=None,
    priority=None,
    category=None,
    assigned_agent=None,
    customer_tier=None,
    overdue_only=False,
    keyword=None
):
    """
    Dynamic ticket search using parameterized SQL.
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

    if category:
        query += " AND category = ?"
        params.append(category)

    if assigned_agent:
        query += " AND assigned_agent = ?"
        params.append(assigned_agent)

    if customer_tier:
        query += " AND customer_tier = ?"
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

    if overdue_only:

        query += """
        AND due_at < CURRENT_TIMESTAMP
        AND status NOT IN ('Resolved','Closed')
        """

    return fetch_all(query, tuple(params))


def update_ticket_status_db(
    ticket_id: str,
    new_status: str
):

    query = """
    UPDATE tickets
    SET status = ?
    WHERE ticket_id = ?
    """

    rows = execute_write(
        query,
        (new_status, ticket_id)
    )

    return rows > 0



def add_ticket_comment_db(
    ticket_id: str,
    comment_text: str,
    author: str = "AI_AGENT"
):

    query = """
    INSERT INTO ticket_comments
    (
        ticket_id,
        comment_text,
        author
    )
    VALUES
    (
        ?,
        ?,
        ?
    )
    """

    return execute_write(
        query,
        (
            ticket_id,
            comment_text,
            author
        )
    )



def save_conversation_log(
    session_id: str,
    user_message: str,
    agent_response: str,
    tools_used: str
):

    query = """
    INSERT INTO conversation_logs
    (
        session_id,
        user_message,
        agent_response,
        tools_used
    )
    VALUES
    (
        ?, ?, ?, ?
    )
    """

    execute_write(
        query,
        (
            session_id,
            user_message,
            agent_response,
            tools_used
        )
    )


def recall_conversation_db(
    keyword: str
):

    query = """
    SELECT *
    FROM conversation_logs
    WHERE
        user_message LIKE ?
        OR agent_response LIKE ?
    ORDER BY created_at DESC
    LIMIT 20
    """

    return fetch_all(
        query,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )


def save_archival_memory_db(
    memory_key: str,
    memory_value: str,
    memory_type: str,
    importance: int
):

    query = """
    INSERT INTO archival_memory
    (
        memory_key,
        memory_value,
        memory_type,
        importance
    )
    VALUES
    (
        ?, ?, ?, ?
    )
    """

    execute_write(
        query,
        (
            memory_key,
            memory_value,
            memory_type,
            importance
        )
    )


def recall_archival_memory_db():

    query = """
    SELECT *
    FROM archival_memory
    ORDER BY importance DESC
    """

    return fetch_all(query)



def save_summary_db(
    session_id: str,
    summary: str,
    key_decisions: str,
    open_items: str
):

    query = """
    INSERT INTO conversation_summaries
    (
        session_id,
        summary,
        key_decisions,
        open_items
    )
    VALUES
    (
        ?, ?, ?, ?
    )
    """

    execute_write(
        query,
        (
            session_id,
            summary,
            key_decisions,
            open_items
        )
    )



def write_audit_log(
    tool_name: str,
    tool_input: str,
    tool_output: str,
    status: str
):

    query = """
    INSERT INTO tool_audit_logs
    (
        tool_name,
        input,
        output,
        status
    )
    VALUES
    (
        ?, ?, ?, ?
    )
    """

    execute_write(
        query,
        (
            tool_name,
            tool_input,
            tool_output,
            status
        )
    )



def get_open_tickets():

    query = """
    SELECT *
    FROM open_tickets
    """

    return fetch_all(query)


def get_overdue_tickets():

    query = """
    SELECT *
    FROM overdue_tickets
    """

    return fetch_all(query)


def get_ticket_work_queue():

    query = """
    SELECT *
    FROM ticket_work_queue
    """

    return fetch_all(query)