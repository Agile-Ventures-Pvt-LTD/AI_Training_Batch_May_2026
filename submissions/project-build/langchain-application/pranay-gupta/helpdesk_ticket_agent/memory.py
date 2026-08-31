from datetime import datetime

from db_utils import (execute_select_query, execute_single_record_query, execute_update_query)


def save_conversation_log(session_id: str,user_message: str,agent_response: str,tools_used: str = ""):
    query = """
    INSERT INTO conversation_logs
    (
        session_id,
        user_message,
        agent_response,
        tools_used
    )
    VALUES (?, ?, ?, ?)
    """

    return execute_update_query(
        query,
        (
            session_id,
            user_message,
            agent_response,
            tools_used
        )
    )


def get_recent_conversations(session_id: str,limit: int = 5):
    query = """
    SELECT *
    FROM conversation_logs
    WHERE session_id = ?
    ORDER BY created_at DESC
    LIMIT ?
    """

    return execute_select_query(query,
        (session_id, limit)
    )


def search_conversation_history(keyword: str):
    pattern = f"%{keyword}%"

    query = """
    SELECT *
    FROM conversation_logs
    WHERE user_message LIKE ?
       OR agent_response LIKE ?
    ORDER BY created_at DESC
    """

    return execute_select_query(query,
        (pattern, pattern)
    )


def save_archival_memory(memory_key: str,memory_value: str,memory_type: str = "preference",importance: int = 3):
    existing = get_archival_memory(memory_key)

    if existing:

        query = """
        UPDATE archival_memory
        SET
            memory_value = ?,
            memory_type = ?,
            importance = ?,
            updated_at = ?
        WHERE memory_key = ?
        """

        return execute_update_query(query,
            (
                memory_value,
                memory_type,
                importance,
                datetime.now().isoformat(),
                memory_key
            )
        )

    query = """
    INSERT INTO archival_memory
    (
        memory_key,
        memory_value,
        memory_type,
        importance
    )
    VALUES (?, ?, ?, ?)
    """

    return execute_update_query(query,
        (
            memory_key,
            memory_value,
            memory_type,
            importance
        )
    )


def get_archival_memory(memory_key: str):
    query = """
    SELECT *
    FROM archival_memory
    WHERE memory_key = ?
    """

    return execute_single_record_query(query,
        (memory_key,)
    )


def get_all_archival_memories():
    query = """
    SELECT *
    FROM archival_memory
    ORDER BY importance DESC
    """

    return execute_select_query(query)


def save_conversation_summary(session_id: str,summary: str,key_decisions: str = "",open_items: str = ""):
    query = """
    INSERT INTO conversation_summaries
    (
        session_id,
        summary,
        key_decisions,
        open_items
    )
    VALUES (?, ?, ?, ?)
    """

    return execute_update_query(query,
        (
            session_id,
            summary,
            key_decisions,
            open_items
        )
    )


def get_latest_summary(session_id: str):
    query = """
    SELECT *
    FROM conversation_summaries
    WHERE session_id = ?
    ORDER BY created_at DESC
    LIMIT 1
    """

    return execute_single_record_query(query,
        (session_id,)
    )


def log_tool_usage(session_id: str,tool_name: str,tool_input: str,tool_output: str):
    query = """
    INSERT INTO tool_audit_logs
    (
        session_id,
        tool_name,
        tool_input,
        tool_output
    )
    VALUES (?, ?, ?, ?)
    """

    return execute_update_query(query,
        (
            session_id,
            tool_name,
            tool_input,
            tool_output
        )
    )