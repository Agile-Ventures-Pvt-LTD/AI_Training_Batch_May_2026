from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from config import (
    GROQ_MODEL,
    GROQ_API_KEY,
    SESSION_ID
)

from db_utils import (
    save_conversation_log,
    recall_conversation_db,
    save_archival_memory_db,
    recall_archival_memory_db,
    save_summary_db
)



llm = ChatGroq(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0
)




def save_conversation_memory(
    user_message: str,
    agent_response: str,
    tools_used: str
):
    """
    Store every interaction.
    """

    save_conversation_log(
        session_id=SESSION_ID,
        user_message=user_message,
        agent_response=agent_response,
        tools_used=tools_used
    )

    return {
        "stored": True
    }


def recall_conversation_memory(
    keyword: str
):
    """
    Search previous conversations.
    """

    records = recall_conversation_db(
        keyword
    )

    return {
        "count": len(records),
        "results": records
    }



def save_archival_memory(
    memory_key: str,
    memory_value: str,
    memory_type: str = "preference",
    importance: int = 5
):
    """
    Store durable user preference.
    """

    save_archival_memory_db(
        memory_key=memory_key,
        memory_value=memory_value,
        memory_type=memory_type,
        importance=importance
    )

    return {
        "success": True,
        "memory_key": memory_key
    }



def recall_archival_memory():
    """
    Retrieve long-term memory.
    """

    memories = recall_archival_memory_db()

    return {
        "count": len(memories),
        "memories": memories
    }



def build_conversation_text(
    conversation_rows
):
    """
    Convert DB rows to text.
    """

    chunks = []

    for row in conversation_rows:

        chunks.append(
            f"""
USER:
{row['user_message']}

AGENT:
{row['agent_response']}
"""
        )

    return "\n".join(chunks)



SUMMARY_PROMPT = """
You are a helpdesk operations analyst.

Summarize the conversation.

Return:

1. Summary
2. Key Decisions
3. Open Items

Format:

SUMMARY:
...

KEY_DECISIONS:
...

OPEN_ITEMS:
...
"""


def generate_conversation_summary(
    conversation_rows
):
    """
    Uses Groq to summarize.
    """

    conversation_text = build_conversation_text(
        conversation_rows
    )

    response = llm.invoke(
        [
            HumanMessage(
                content=
                SUMMARY_PROMPT
                + "\n\n"
                + conversation_text
            )
        ]
    )

    return response.content



def parse_summary_sections(
    summary_text: str
):
    """
    Extract sections from summary.
    """

    summary = ""
    decisions = ""
    open_items = ""

    current = None

    for line in summary_text.splitlines():

        line = line.strip()

        if line.startswith("SUMMARY"):
            current = "summary"
            continue

        elif line.startswith("KEY_DECISIONS"):
            current = "decisions"
            continue

        elif line.startswith("OPEN_ITEMS"):
            current = "open_items"
            continue

        if current == "summary":
            summary += line + "\n"

        elif current == "decisions":
            decisions += line + "\n"

        elif current == "open_items":
            open_items += line + "\n"

    return {
        "summary": summary.strip(),
        "key_decisions": decisions.strip(),
        "open_items": open_items.strip()
    }



def summarize_and_store_conversation(
    keyword: str = ""
):
    """
    Summarize conversation history
    and store in DB.
    """

    rows = recall_conversation_db(
        keyword
    )

    if not rows:

        return {
            "stored": False,
            "message": "No conversation found."
        }

    summary_text = generate_conversation_summary(
        rows
    )

    parsed = parse_summary_sections(
        summary_text
    )

    save_summary_db(
        session_id=SESSION_ID,
        summary=parsed["summary"],
        key_decisions=parsed["key_decisions"],
        open_items=parsed["open_items"]
    )

    return {
        "stored": True,
        "summary": parsed["summary"],
        "key_decisions": parsed["key_decisions"],
        "open_items": parsed["open_items"]
    }



def detect_preference_statement(
    text: str
):
    """
    Detect if user is trying to save memory.

    Example:
    Remember that I want enterprise
    customers prioritized first.
    """

    triggers = [
        "remember",
        "save this",
        "preference",
        "always prioritize",
        "keep in mind"
    ]

    lower_text = text.lower()

    return any(
        trigger in lower_text
        for trigger in triggers
    )



def get_user_preferences():
    """
    Convenience helper for prioritization tool.
    """

    memory = recall_archival_memory()

    return memory.get(
        "memories",
        []
    )