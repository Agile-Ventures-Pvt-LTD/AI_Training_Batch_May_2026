from db_utils import execute_update
from db_utils import execute_query


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
      tools_used
    )
    VALUES
    (?, ?, ?, ?)
    """

    execute_update(
        query,
        (
            session_id,
            user_message,
            agent_response,
            tools_used
        )
    )