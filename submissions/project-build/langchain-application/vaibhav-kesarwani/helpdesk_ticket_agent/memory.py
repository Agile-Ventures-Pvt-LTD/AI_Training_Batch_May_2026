from db_utils import get_connection


def save_conversation_db(
    session_id,
    user_message,
    agent_response,
    tools_used=""
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversation_logs
        (
            session_id,
            user_message,
            agent_response,
            tools_used
        )
        VALUES (?, ?, ?, ?)
    """, (
        session_id,
        user_message,
        agent_response,
        tools_used
    ))

    conn.commit()
    conn.close()

    return "Conversation saved"


def recall_conversation_db(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM conversation_logs
        WHERE
            user_message LIKE ?
            OR agent_response LIKE ?
        ORDER BY id DESC
        LIMIT 20
    """, (
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    rows = cursor.fetchall()
    conn.close()

    return rows


def save_archival_memory_db(
    memory_key,
    memory_value,
    memory_type="preference",
    importance=5
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO archival_memory
        (
            memory_key,
            memory_value,
            memory_type,
            importance
        )
        VALUES (?, ?, ?, ?)
    """, (
        memory_key,
        memory_value,
        memory_type,
        importance
    ))

    conn.commit()
    conn.close()

    return "Memory saved"


def recall_archival_memory_db(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM archival_memory
        WHERE
            memory_key LIKE ?
            OR memory_value LIKE ?
        ORDER BY importance DESC
    """, (
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    rows = cursor.fetchall()
    conn.close()

    return rows


def save_summary_db(
    session_id,
    summary,
    key_decisions="",
    open_items=""
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversation_summaries
        (
            session_id,
            summary,
            key_decisions,
            open_items
        )
        VALUES (?, ?, ?, ?)
    """, (
        session_id,
        summary,
        key_decisions,
        open_items
    ))

    conn.commit()
    conn.close()

    return "Summary saved"