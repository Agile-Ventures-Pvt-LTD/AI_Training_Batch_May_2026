from datetime import datetime

from db_utils import (
    fetch_all,
    execute_query
)


def save_conversation(
        session_id,
        user_message,
        agent_response,
        tools_used
):

    query = """

    INSERT INTO conversation_logs
    (
    session_id,
    user_message,
    agent_response,
    tools_used,
    created_at
    )

    VALUES (?,?,?,?,?)

    """

    execute_query(
        query,
        (
            session_id,
            user_message,
            agent_response,
            str(tools_used),
            datetime.now().isoformat()
        )
    )


    return {
        "status":"saved"
    }



def recall_conversation(keyword):


    query = """

    SELECT *
    FROM conversation_logs
    WHERE user_message LIKE ?

    ORDER BY created_at DESC

    LIMIT 5

    """


    result = fetch_all(
        query,
        (
            f"%{keyword}%",
        )
    )


    return result


def save_archival_memory(
        memory_key,
        memory_value,
        memory_type="preference",
        importance=5
):


    query = """

    INSERT INTO archival_memory
    (
    memory_key,
    memory_value,
    memory_type,
    importance,
    created_at
    )

    VALUES (?,?,?,?,?)

    """



    execute_query(
        query,
        (
            memory_key,
            memory_value,
            memory_type,
            importance,
            datetime.now().isoformat()
        )
    )


    return {
        "message":
        "Preference saved successfully"
    }



def recall_archival_memory():


    query = """

    SELECT *
    FROM archival_memory
    ORDER BY importance DESC

    """


    return fetch_all(query)


def save_summary(
        session_id,
        summary,
        decisions,
        open_items
):


    query = """

    INSERT INTO conversation_summaries
    (
    session_id,
    summary,
    key_decisions,
    open_items,
    created_at
    )

    VALUES (?,?,?,?,?)

    """



    execute_query(
        query,
        (
            session_id,
            summary,
            decisions,
            open_items,
            datetime.now().isoformat()
        )
    )


    return {
        "stored":True
    }