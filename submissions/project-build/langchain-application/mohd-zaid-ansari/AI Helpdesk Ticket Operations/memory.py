from db_utils import fetch_one, fetch_all, execute_write
from datetime import datetime
from typing import Dict, List, Optional, Any

def save_conversation_log(session_id: str, user_message: str, agent_response: str, tools_used: str):
    query = """
        Insert into conversation_logs(session_id, user_message, agent_response, tools_used, created_at)
        VALUES (?, ?, ?, ?, ?)
    """

    execute_write(
        query,
        (session_id, user_message, agent_response, tools_used, datetime.now().isoformat())
    )

    return {"saved": True, "session_id": session_id}

def recall_conversation(session_id: str = None, keyword: str = None):
    query = """
        Select session_id, user_message, agent_response, tools_used, created_at from conversation_logs
        where 1=1
    """
    params = []
    if session_id:
        query += " AND session_id = ?"
        params.append(session_id)
    if keyword:
        query += " AND user_message LIKE ?"
        params.append(f"%{keyword}%")
    return fetch_all(query, params)

def save_archival_memory(memory_key: str, memory_value: str, memory_type: str = "preference", importance: int = 3):
    query = """
        Insert into archival_memory (memory_key, memory_value, memory_type, importance, created_at)
        Values (?, ?, ?, ?, ?)
    """
    execute_write(
        query,
        (memory_key, memory_value, memory_type, importance, datetime.now().isoformat())
    )
    return {"saved": True, "memory_key": memory_key}

def recall_archival_memory(memory_key: str):
    query = """
        Select memory_key, memory_value, memory_type, importance from archival_memory Where memory_key = ?
    """
    result = fetch_one(query, (memory_key,))
    if not result:
        return {"found": False, "message": "No memory found"}
    return {
        "found": True,
        "memory_key": result["memory_key"],
        "memory_value": result["memory_value"],
        "memory_type": result["memory_type"],
        "importance": result["importance"]
    }

def store_summary(session_id: str, summary: str, key_decisions: str, open_items: str):
    query = """
        Insert into conversation_summaries (session_id, summary, key_decisions, open_items, stored_at) Values (?, ?, ?, ?, ?)
    """
    execute_write(
        query,
        (session_id, summary, key_decisions, open_items, datetime.now().isoformat())
    )
    return {"stored": True, "session_id": session_id}