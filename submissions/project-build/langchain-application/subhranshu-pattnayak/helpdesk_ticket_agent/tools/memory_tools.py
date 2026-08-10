from database.connection import get_connection
from langchain.tools import tool

@tool
def save_conversation(
    session_id: str,
    user_message: str,
    agent_response: str,
    tools_used: str
):
    """
    Save a conversation turn to recall memory (conversation log).
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversation_logs
        (
            session_id,
            user_message,
            agent_response,
            tools_used
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            session_id,
            user_message,
            agent_response,
            tools_used
        )
    )

    conn.commit()

    inserted_id = cursor.lastrowid

    conn.close()

    return {
        "status": "success",
        "conversation_id": inserted_id,
        "session_id": session_id
    }



@tool
def recall_conversation(
    keyword: str
):
    """
    Retrieve previous conversations containing a keyword.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            session_id,
            user_message,
            agent_response,
            tools_used,
            created_at
        FROM conversation_logs
        WHERE user_message LIKE ?
            OR agent_response LIKE ?
        ORDER BY created_at DESC
        LIMIT 20
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

@tool
def save_archival_memory(
    memory_key: str,
    memory_value: str,
    memory_type: str = "preference",
    importance: int = 3
):
    """
    Save a long-term memory such as user preferences, business rules,
    priorities, or important facts.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO archival_memory
        (
            memory_key,
            memory_value,
            memory_type,
            importance
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            memory_key,
            memory_value,
            memory_type,
            importance
        )
    )

    conn.commit()

    memory_id = cursor.lastrowid

    conn.close()

    return {
        "status": "success",
        "memory_id": memory_id,
        "memory_key": memory_key
    }




@tool
def recall_archival_memory(
    memory_key: str = ""
):
    """
    Retrieve long-term memories such as preferences, business rules,
    priorities, or important facts.
    """

    conn = get_connection()
    cursor = conn.cursor()

    if memory_key.strip():

        cursor.execute(
            """
            SELECT
                memory_key,
                memory_value,
                memory_type,
                importance,
                created_at
            FROM archival_memory
            WHERE memory_key LIKE ?
            ORDER BY importance DESC
            """,
            (f"%{memory_key}%",)
        )

    else:

        cursor.execute(
            """
            SELECT
                memory_key,
                memory_value,
                memory_type,
                importance,
                created_at
            FROM archival_memory
            ORDER BY importance DESC
            LIMIT 20
            """
        )

    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    result = [
        dict(zip(columns, row))
        for row in rows
    ]

    conn.close()

    return result

