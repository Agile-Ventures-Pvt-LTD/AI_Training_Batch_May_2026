import json
from langchain_core.tools import tool
from langchain_groq import ChatGroq
import db_utils
import config

@tool
def s_archival_memory(key: str,pre_txt: str):
    """Save a long-term user preference or business rule (e.g., 'prioritize enterprise customers')."""
    q = "INSERT INTO archival_memory (memory_key, memory_value, memory_type) VALUES (?, ?, 'preference')"
    res = db_utils.write_db(q, (key, pre_txt), "save_archival_memory", pre_txt)
    save = "Preference saved to archival memory."
    return save

@tool
def recall_archival_memory():
    """Retrieve all saved user preferences and rules to influence prioritization."""
    res = db_utils.read_db("SELECT memory_key, memory_value FROM archival_memory")
    json_return = json.dumps(res)
    return json_return

@tool
def recall_convo(keyword: str):
    """Search past conversations for a specific keyword."""
    q = "SELECT user_message, agent_response FROM conversation_logs WHERE user_message LIKE ? OR agent_response LIKE ? LIMIT 5"
    like_kw = f"%{keyword}%"
    res = db_utils.read_db(q, (like_kw, like_kw))
    json_return = json.dumps(res)
    return json_return

@tool
def sumarize_convo(session_id: str):
    """Summarize the current conversation history and store it in the database."""
    logs = db_utils.read_db(
        "SELECT user_message, agent_response FROM conversation_logs WHERE session_id = ?", 
        (session_id,)
    )
    if not logs:
        return "No conversation logs found to summarize."

    llm = ChatGroq(model=config.GROQ_MODEL, api_key=config.GROQ_API_KEY, temperature=0.3)
    chat_text = "\n".join([f"User: {l['user_message']}\nAgent: {l['agent_response']}" for l in logs])
    
    prompt = f"Summarize this conversation. Extract key or important decisions and open items.\n\n{chat_text}"
    summary = llm.invoke(prompt).content

    q = "INSERT INTO conversation_summaries (session_id, summary, key_decisions, open_items) VALUES (?, ?, 'Extracted by Groq', 'Pending review')"
    db_utils.write_db(q, (session_id, summary), "summarize_conversation", session_id)
    
    return "Conversation summarized and saved successfully."

def log_convo_turn(session_id, user_msg, agent_resp, tools_used):
    q = "INSERT INTO conversation_logs (session_id, user_message, agent_response, tools_used) VALUES (?, ?, ?, ?)"
    db_utils.write_db(q, (session_id, user_msg, agent_resp, json.dumps(tools_used)), "log_conversation", session_id)