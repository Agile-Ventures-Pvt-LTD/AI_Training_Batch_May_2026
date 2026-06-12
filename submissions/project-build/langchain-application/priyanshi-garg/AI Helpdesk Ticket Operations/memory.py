from db_utils import execute_query

from tools import (
    save_conversation,
    save_archival_memory,
    recall_archival_memory,
    recall_conversation,
    summarize_conversation
)


def log_chat(user_message, agent_response):

    save_conversation.invoke({
        "user_message": user_message,
        "agent_response": agent_response
    })


def save_preference(key, value):

    return save_archival_memory.invoke({
        "memory_key": key,
        "memory_value": value
    })


def get_preference():

    return recall_archival_memory.invoke({})


def get_past_conversation(keyword):

    return recall_conversation.invoke({
        "keyword": keyword
    })


def save_summary(summary):

    return summarize_conversation.invoke(
        {
            "session_id": "default",
            "summary": summary,
            "key_decisions": "",
            "open_items": ""
        }
    )


def get_recent_logs():

    return execute_query(
        """
        SELECT *
        FROM conversation_logs
        ORDER BY id DESC
        LIMIT 20
        """
    )