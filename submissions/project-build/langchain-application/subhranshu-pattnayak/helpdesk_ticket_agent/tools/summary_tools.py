from database.connection import get_connection
from langchain.tools import tool
from langchain_groq import ChatGroq

@tool
def summarize_conversation(
    session_id: str
):
    """
    Generate and store a structured summary of a conversation session.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            user_message,
            agent_response,
            tools_used
        FROM conversation_logs
        WHERE session_id = ?
        ORDER BY created_at
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    if not rows:
        conn.close()

        return {
            "status": "error",
            "message": f"No conversation found for session '{session_id}'"
        }

    conversation_text = "\n\n".join(
        [
            f"User: {user_message}\n"
            f"Agent: {agent_response}\n"
            f"Tools Used: {tools_used}"
            for user_message, agent_response, tools_used in rows
        ]
    )

    summarizer_llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    prompt = f"""
    You are a conversation summarizer.

    Analyze the conversation and return EXACTLY in the format:

    SUMMARY:
    <summary>

    KEY_DECISIONS:
    <key decisions>

    OPEN_ITEMS:
    <open items>

    Conversation:
    {conversation_text}
    """

    response = summarizer_llm.invoke(prompt)

    content = response.content

    summary = ""
    key_decisions = ""
    open_items = ""

    try:
        sections = content.split("KEY_DECISIONS:")

        summary = sections[0].replace(
            "SUMMARY:",
            ""
        ).strip()

        remaining = sections[1].split("OPEN_ITEMS:")

        key_decisions = remaining[0].strip()

        open_items = remaining[1].strip()

    except Exception:
        summary = content

    cursor.execute(
        """
        INSERT INTO conversation_summaries
        (
            session_id,
            summary,
            key_decisions,
            open_items
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            session_id,
            summary,
            key_decisions,
            open_items
        )
    )

    conn.commit()

    summary_id = cursor.lastrowid

    conn.close()

    return {
        "status": "success",
        "summary_id": summary_id,
        "session_id": session_id,
        "summary": summary,
        "key_decisions": key_decisions,
        "open_items": open_items
    }