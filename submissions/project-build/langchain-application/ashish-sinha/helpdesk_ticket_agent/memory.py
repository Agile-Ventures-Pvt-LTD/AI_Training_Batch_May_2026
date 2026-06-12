from db_utils import fetching_all,execution_query

def saving_converstation(session_id:str,user_message:str,agent_response:str,tools_used:str):
    query = """
INSERT INTO conversation_logs
    (
        session_id,
        user_message,
        agent_response,
        tools_used,
        created_at
    )
    VALUES
    (
        ?, ?, ?, ?, CURRENT_TIMESTAMP
    )
"""
    
    execution_query(
        query,
        (session_id,user_message,agent_response,tools_used)
    )

    return{
        "Success": True
    }

def recalling_coversation(keyword:str):

    query = """
    SELECT *
    FROM conversation_logs
    WHERE user_message LIKE ?
       OR agent_response LIKE ?
    ORDER BY created_at DESC
    LIMIT 15
    """
    keyword = f"%{keyword}"

    return fetching_all(
        query,
        (keyword,keyword))

def saving_archival_memory(memory_key:str,memory_value:str,memory_type:str,importance:str):

    query = """
    INSERT INTO archival_memory
    (
        memory_key,
        memory_value,
        memory_type,
        importance,
        created_at
    )
    VALUES
    (
        ?, ?, ?, ?, CURRENT_TIMESTAMP
    )
    """

    execution_query(
        query,
        (memory_key,memory_value,memory_type,importance)
    )

    return {
        "success": True
    }

def recall_archival_memory():

    query = """
    SELECT *
    FROM archival_memory
    ORDER BY importance DESC,
             created_at DESC
    """

    return fetching_all(query)

def saving_conversation_summary(session_id:str,summary:str,key_decisions:str,open_items:str):

    query = """
    INSERT INTO conversation_summaries
    (
        session_id,
        summary,
        key_decisions,
        open_items,
        created_at
    )
    VALUES
    (
        ?, ?, ?, ?, CURRENT_TIMESTAMP
    )
    """

    execution_query(
        query,
        (session_id,summary,key_decisions,open_items)
    )

    return {
        "success":True
    }

def getting_recent_conversation(session_id:str):

    query = """
    SELECT *
    FROM conversation_logs
    WHERE session_id = ?
    ORDER BY created_at DESC
    LIMIT 20
    """

    return fetching_all(
        query,
        (session_id,)
    )