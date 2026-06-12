from db_utils import execute_select
from db_utils import execute_write


def save_conversation(
        session_id,
        user_message,
        agent_response,
        tools_used
):
    execute_write(
        """
        INSERT INTO conversation_logs
        (
        session_id,
        user_message,
        agent_response,
        tools_used
        )
        VALUES (?,?,?,?)
        """,
        (
            session_id,
            user_message,
            agent_response,
            tools_used
        )
    )

    return "saved"


def recall_conversation(keyword):

    rows = execute_select(
        """
        SELECT *
        FROM conversation_logs
        WHERE user_message LIKE ?
        OR agent_response LIKE ?
        ORDER BY created_at DESC
        LIMIT 10
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    return rows


def save_archival_memory(
        key,
        value,
        memory_type="preference",
        importance=5
):
    execute_write(
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
            key,
            value,
            memory_type,
            importance
        )
    )

    return "memory_saved"


def recall_archival_memory():
    return execute_select(
        """
        SELECT *
        FROM archival_memory
        ORDER BY importance DESC
        """
    )