import json
from datetime import datetime

from langchain_core.tools import tool

from config import (
    ALLOWED_STATUSES,
    PRIORITY_SCORES,
    CUSTOMER_TIER_SCORES
)

from db_utils import (
    search_tickets_db,
    get_ticket_by_id,
    get_ticket_comments,
    ticket_exists,
    update_ticket_status_db,
    add_ticket_comment_db,
    write_audit_log
)

from memory import (
    save_conversation_memory,
    recall_conversation_memory,
    save_archival_memory,
    recall_archival_memory,
    summarize_and_store_conversation,
    get_user_preferences
)

import json

@tool
def search_tickets(query: str):
    """Search tickets using keyword."""

    results = search_tickets_db(
        keyword=query
    )

    return json.dumps(
        results,
        indent=2,
        default=str
    )


@tool
def get_ticket_details(ticket_id: str):
    """Get details of a ticket."""

    results = get_ticket_by_id(
        {
            "keyword": ticket_id
        }
        
    )
    if not results:
        return f"Ticket {ticket_id} not found."

    return json.dumps(results, indent=2, default=str)



@tool
def get_ticket_comments_tool(ticket_id: str):
    """Get comments for a ticket."""

    results = get_ticket_comments(
        {
            ticket_id
        }
    )
    return json.dumps(results, indent=2, default=str)


@tool
def calculate_sla_status(ticket_id: str):
    """Calculate SLA status for a ticket."""

    ticket = get_ticket_by_id(ticket_id)

    if not ticket:
        return "Ticket not found."

    due_at = ticket.get("due_at")

    if not due_at:
        return json.dumps(
            {
                "ticket_id": ticket_id,
                "sla_status": "UNKNOWN"
            },
            indent=2,
            default=str
        )

    try:
        due_date = datetime.fromisoformat(str(due_at))
    except Exception:
        return json.dumps(
            {
                "ticket_id": ticket_id,
                "sla_status": "UNKNOWN"
            },
            indent=2,
            default=str
        )

    now = datetime.now()

    if due_date < now:
        sla_status = "BREACHED"
    elif due_date.date() == now.date():
        sla_status = "DUE_TODAY"
    else:
        sla_status = "WITHIN_SLA"

    return json.dumps(
        {
            "ticket_id": ticket_id,
            "sla_status": sla_status,
            "due_at": due_at
        },
        indent=2,
        default=str
    )

tickets = search_tickets_db(
    status="Open"
)


@tool
def update_ticket_status(input_text: str):
    """
    Update ticket status.

    Format:
    TICKET_ID|NEW_STATUS
    """

    try:
        ticket_id, new_status = input_text.split("|")
    except Exception:
        return "Format must be TICKET_ID|NEW_STATUS"

    if new_status not in ALLOWED_STATUSES:
        return "Invalid status."

    ticket = get_ticket_by_id(ticket_id)

    if not ticket:
        return "Ticket not found."

    update_ticket_status_db(
        ticket_id,
        new_status
    )

    write_audit_log(
        "update_ticket_status",
        input_text,
        "Updated",
        "SUCCESS"
    )

    return json.dumps(
        {
            "success": True,
            "ticket_id": ticket_id,
            "new_status": new_status
        },
        indent=2
    )

@tool
def add_ticket_comment(input_text: str):
    """
    Add comment.

    Format:
    TICKET_ID|COMMENT
    """

    try:
        ticket_id, comment = input_text.split("|", 1)
    except Exception:
        return "Format must be TICKET_ID|COMMENT"

    if not ticket_exists(ticket_id):
        return "Ticket not found."

    add_ticket_comment_db(
        ticket_id=ticket_id,
        comment_text=comment,
        author="AI_AGENT"
    )

    write_audit_log(
        "add_ticket_comment",
        comment,
        "Inserted",
        "SUCCESS"
    )

    return json.dumps(
        {
            "success": True,
            "ticket_id": ticket_id,
            "comment_added": True
        },
        indent=2
    )

@tool
def save_conversation(input_text: str):
    """
    Save conversation.

    Format:
    user_message|agent_response|tools_used
    """

    try:
        user_message, agent_response, tools_used = input_text.split("|", 2)
    except Exception:
        return "Invalid format."

    result = save_conversation_memory(
        user_message,
        agent_response,
        tools_used
    )

    return json.dumps(
        {
            "success": True,
            "result": result
        },
        indent=2,
        default=str
    )

@tool
def save_user_preference(input_text: str):
    """
    Save preference.

    Format:
    key|value
    """

    try:
        key, value = input_text.split("|", 1)
    except Exception:
        return "Format must be key|value"

    return save_archival_memory(
        memory_key=key,
        memory_value=value,
        memory_type="preference",
        importance=5
    )


@tool
def recall_user_preferences(keyword: str):
    """Recall conversation memory."""

    result = recall_conversation_memory(keyword)

    return json.dumps(
        result,
        indent=2,
        default=str
    )

@tool
def summarize_conversation(keyword: str = ""):
    """Summarize stored conversations."""

    result = summarize_and_store_conversation(keyword)

    return json.dumps(
        result,
        indent=2,
        default=str
    )


TOOLS = [
    search_tickets,
    get_ticket_details,
    get_ticket_comments_tool,
    calculate_sla_status,
    update_ticket_status,
    add_ticket_comment,
    save_conversation,
    save_user_preference,
    recall_user_preferences,
    summarize_conversation
]