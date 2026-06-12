# memory.py

from langchain.tools import tool
from db_utils import run_query

# Save memory tool

@tool
def save_memory(memory_key: str, memory_value: str):
    """
    Save user preference.
    """
    
    run_query("""
        INSERT INTO archival_memory
        (memory_key, memory_value) VALUES (?, ?)
        """, 
        (memory_key, memory_value))

    return {"message": "Memory Saved"}
    
# Recall memory tool

@tool
def recall_memory(keyword: str):
    """
    Recall memory.
    """

    result = run_query(
        """
        SELECT memory_key, memory_value
        FROM archival_memory
        WHERE memory_key LIKE ?
        OR memory_value LIKE ?
        LIMIT 10
        """,
        (f"%{keyword}%", f"%{keyword}%")
    )

    return {"memory": result}

# Save conversation tool

@tool
def save_conversation(user_message: str, agent_response: str):
    """
    Save conversation.
    """

    run_query(
        """
        INSERT INTO conversation_logs
        (session_id, user_message, agent_response)
        VALUES
        ('session_001', ?, ?)
        """,
        (user_message, agent_response)
    )

    return {"message": "Conversation Saved"}

# Recall conversation tool

@tool
def recall_conversation(keyword: str):
    """
    Recall previous conversations.
    """

    result = run_query(
        """
        SELECT user_message, agent_response
        FROM conversation_logs
        WHERE user_message LIKE ?
        OR agent_response LIKE ?
        LIMIT 10
        """,
        (f"%{keyword}%", f"%{keyword}%")
    )

    return {"conversations": result}

@tool
def summarize_conversation(dummy: str = ""):
    """
    Summarize conversation and store in memory.
    """

    conversations = run_query(
        """
        SELECT user_message, agent_response
        FROM conversation_logs
        LIMIT 10
        """
    )
    summary = str(conversations)
    run_query(
        """
        INSERT INTO conversation_summaries
        (session_id, summary)
        VALUES('session_001', ?)
        """, (summary,)
    )

    return {"message": "Conversation summary stored"}