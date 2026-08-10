from langchain.tools import tool

from db_utils import (
    search_tickets_db,
    get_ticket_details_db,
    get_ticket_comments_db,
    get_overdue_tickets_db,
    get_ticket_work_queue_db,
    calculate_sla_status_db,
    update_ticket_status_db,
    add_comment_db,
    audit_log_db
)

from memory import (
    save_archival_memory,
    recall_archival_memory,
    recall_conversation,
    summarize_conversation
)

from config import VALID_STATUSES




@tool
def search_tickets(
    status: str = None,
    priority: str = None,
    category: str = None,
    assigned_to: str = None,
    customer_tier: str = None,
    keyword: str = None,
    overdue_only: bool = False
):
    """
    Search tickets using filters.
    """

    tickets = search_tickets_db(
        status=status,
        priority=priority,
        category=category,
        assigned_to=assigned_to,
        customer_tier=customer_tier,
        keyword=keyword,
        overdue_only=overdue_only
    )

    if not tickets:
        return {
            "success": True,
            "count": 0,
            "tickets": [],
            "message": "No matching tickets found"
        }

    return {
        "success": True,
        "count": len(tickets),
        "tickets": tickets
    }




@tool
def get_ticket_details(ticket_id: str):
    """
    Get complete ticket details.
    """

    ticket = get_ticket_details_db(ticket_id)

    if not ticket:
        return {
            "success": False,
            "error": "Ticket not found"
        }

    return {
        "success": True,
        "ticket": ticket
    }




@tool
def get_ticket_comments(ticket_id: str):
    """
    Get ticket comments.
    """

    comments = get_ticket_comments_db(ticket_id)

    return {
        "success": True,
        "ticket_id": ticket_id,
        "comment_count": len(comments),
        "comments": comments
    }




@tool
def get_overdue_tickets():
    """
    Return overdue tickets.
    """

    tickets = get_overdue_tickets_db()

    if not tickets:
        return {
            "success": True,
            "count": 0,
            "tickets": [],
            "message": "No overdue tickets found"
        }

    return {
        "success": True,
        "count": len(tickets),
        "tickets": tickets
    }




@tool
def calculate_sla_status(ticket_id: str):
    """
    Calculate SLA status.
    """

    result = calculate_sla_status_db(ticket_id)

    if not result:
        return {
            "success": False,
            "error": "Ticket not found"
        }

    return {
        "success": True,
        "sla": result
    }




@tool
def prioritize_tickets():
    """
    Return top recommended tickets.
    """

    tickets = get_ticket_work_queue_db()

    if not tickets:
        return {
            "success": True,
            "recommended_count": 0,
            "recommendations": []
        }

    recommendations = []

    for ticket in tickets[:10]:

        reasons = []

        if ticket.get("priority") in ["High", "Urgent"]:
            reasons.append("high priority")

        if ticket.get("customer_tier") == "Enterprise":
            reasons.append("enterprise customer")

        if ticket.get("sla_status") == "BREACHED":
            reasons.append("SLA breached")

        recommendations.append({
            "ticket_id": ticket.get("ticket_id"),
            "subject": ticket.get("subject"),
            "reason": ", ".join(reasons)
        })

    return {
        "success": True,
        "recommended_count": len(recommendations),
        "recommendations": recommendations
    }




@tool
def update_ticket_status(
    ticket_id: str,
    new_status: str
):
    """
    Safely update ticket status.
    """

    if new_status not in VALID_STATUSES:

        return {
            "success": False,
            "message": f"Allowed statuses: {VALID_STATUSES}"
        }

    ticket = get_ticket_details_db(ticket_id)

    if not ticket:

        return {
            "success": False,
            "message": "Ticket not found"
        }

    result = update_ticket_status_db(
        ticket_id,
        new_status
    )

    try:
        audit_log_db(
            tool_name="update_ticket_status",
            tool_input={
                "ticket_id": ticket_id,
                "new_status": new_status
            },
            tool_output=result
        )
    except Exception:
        pass

    return result




@tool
def add_ticket_comment(
    ticket_id: str,
    comment: str
):
    """
    Add internal comment.
    """

    ticket = get_ticket_details_db(ticket_id)

    if not ticket:
        return {
            "success": False,
            "message": "Ticket not found"
        }

    result = add_comment_db(
        ticket_id=ticket_id,
        comment=comment
    )

    try:
        audit_log_db(
            tool_name="add_ticket_comment",
            tool_input={
                "ticket_id": ticket_id,
                "comment": comment
            },
            tool_output=result
        )
    except Exception:
        pass

    return result



@tool
def save_user_preference(
    memory_key: str,
    memory_value: str
):
    """
    Save preference.
    """

    return save_archival_memory(
        memory_key=memory_key,
        memory_value=memory_value
    )



@tool
def recall_user_preference(keyword: str):
    """
    Recall preferences.
    """

    return recall_archival_memory(keyword)




@tool
def recall_previous_conversation(keyword: str):
    """
    Recall previous conversation.
    """

    return recall_conversation(keyword)




@tool
def summarize_and_store_conversation(
    session_id: str,
    conversation_text: str
):
    """
    Summarize and store conversation.
    """

    return summarize_conversation(
        session_id=session_id,
        conversation_text=conversation_text
    )




TOOLS = [
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    get_overdue_tickets,
    calculate_sla_status,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
    save_user_preference,
    recall_user_preference,
    recall_previous_conversation,
    summarize_and_store_conversation
]