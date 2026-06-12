# simple memory

def save_conversation(
        session_id,
        user_message,
        agent_response,
        tools_used
):
    """
    Temporary conversation saver.
    Does not use database.
    """

    return {
        "success": True
    }



# CONVERSATION RECALL


def recall_conversation(keyword):

    return {
        "count": 0,
        "results": []
    }



# SAVE PREFERENCE


def save_archival_memory(
        memory_key,
        memory_value,
        memory_type="preference",
        importance=5
):

    return {
        "success": True,
        "memory_key": memory_key,
        "memory_value": memory_value
    }



# RECALL PREFERENCE


def recall_archival_memory(keyword):

    return {
        "count": 0,
        "memories": []
    }



# SUMMARIZE CONVERSATION


def summarize_conversation(
        session_id,
        conversation_text
):

    summary = conversation_text[:500]

    return {
        "stored": True,
        "summary": summary
    }



# AUTO SAVE PREFERENCE


def auto_save_preference(user_message):

    return None



# MEMORY CONTEXT


def build_memory_context():
    """
    Disable memory lookup for now.
    Prevents:
    no such table: archival_memory
    """

    return ""



# USER PREFERENCES


def get_user_preferences():

    return []