from langchain.tools import tool
from datetime import datetime
from db_utils import fetching_all,fetching_one,execution_query
from config import Reference_Time,Valid_Status

from memory import saving_converstation,recalling_coversation,saving_archival_memory,saving_conversation_summary,getting_recent_conversation,recall_archival_memory

@tool
def search_tickets(status:str = None,priority:str = None, category:str = None, assigned_agent:str = None,customer_tier:str = None,overdue_only:str = None):
    """
    Search tickets using filters.
    """

    query = """
    SELECT *
    FROM tickets
    WHERE 1=1
    """
    print(query)
    
    params = []

    if status:
        query += " AND LOWER(status) = LOWER(?)"
        params.append(status)
    
    if priority:
        query += " AND LOWER(priority) = LOWER(?)"
        params.append(priority)

    if category:
        query += " AND LOWER(category) =LOWER(?)"
        params.append(category)

    if assigned_agent:
        query += " AND LOWER(assigned_to) = LOWER(?)"
        params.append(assigned_agent)

    if customer_tier:
        query += " AND LOWER(customer_tier) = LOWER(?)"
        params.append(customer_tier)

    if overdue_only:
        query += " AND due_at < CURRENT_TIMESTAMP"

    # tickets = fetching_all(query,tuple(params))
    print("\nFINAL QUERY:")
    print(query)
    print("PARAMS:", params)

    tickets = fetching_all(query,tuple(params))

    return {
        "count":len(tickets),
        "tickets":tickets[:10]
    }

@tool
def get_ticket_details(ticket_id:str):
    """
    Fetch complete ticket details.
    """

    query = """
    SELECT *
    FROM tickets
    WHERE ticket_id = ?
    """

    ticket = fetching_one(
    query,
    (ticket_id,)
)

    if not ticket:
        return {
            "error": f"Ticket {ticket_id} not found"
        }
    return ticket

@tool
def get_ticket_comments(ticket_id:str):
    """
    Fetch ticket comments and history.
    """

    query = """
    SELECT *
    FROM ticket_comments
    WHERE ticket_id = ?
    ORDER BY created_at
    """

    comments = fetching_all(
    query,
    (ticket_id,)
)

    return {
        "ticket_id": ticket_id,
        "comment_count": len(comments),
        "comments": comments[:10]
    }

@tool
def calculate_sla_status(ticket_id:str):
    """
    Determine SLA status for a ticket.
    """
    ticket = fetching_one(
        """
        SELECT ticket_id,status,due_at
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )

    if not ticket:
        return {
            "error": f"Ticket {ticket_id} not found"
        }

    due_at = ticket.get("due_at")

    if not due_at:
        return {
            "ticket_id": ticket_id,
            "sla_status": "UNKNOWN"
        }

    reference_time = datetime.strptime(
        Reference_Time,
        "%Y-%m-%d %H:%M:%S"
    )

    due_date = datetime.strptime(
        due_at,
        "%Y-%m-%d %H:%M:%S"
    )

    if due_date < reference_time:

        sla_status = "BREACHED"

    elif due_date.date() == reference_time.date():

        sla_status = "DUE_TODAY"

    else:

        sla_status = "WITHIN_SLA"

    return {
        "ticket_id": ticket_id,
        "sla_status": sla_status,
        "due_at": due_at,
        "status": ticket["status"]
    }

@tool
def prioritize_tickets():
    """
    Prioritize open tickets.
    """
    tickets = fetching_all("""
        SELECT *
        FROM ticket_work_queue
        """)
    ranked_tickets = []

    for ticket in tickets:
        score = 0
        if ticket.get("priority") == "Urgent":
            score += 50

        elif ticket.get("priority") == "High":
            score += 30

        if ticket.get("customer_tier") == "Enterprise":
            score += 20

        ranked_tickets.append(
            {
                "score": score,
                **ticket
            }
        )

    ranked_tickets.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "count": len(ranked_tickets),
        "tickets": ranked_tickets[:10]
    }

@tool
def update_ticket_status(ticket_id:str,new_status:str):
    """
    Update Ticket Status
    """

    if new_status not in Valid_Status:
        return{
            "error": f"Invalid status: {new_status}"
        }
    ticket = fetching_one(
        """
        SELECT status
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )
    if not ticket:
        return {
            "error": f"Ticket {ticket_id} not found"
        }
    current_status = ticket["status"]

    if current_status == new_status:
        return {
            "message": "Ticket already in requested status"
        }
    execution_query(
        """
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
        """,
        (
            new_status,
            ticket_id
        )
    )

    execution_query(
        """
        INSERT INTO tool_audit_logs
        (
            tool_name,
            input,
            output,
            status,
            created_at
        )
        VALUES
        (
            ?, ?, ?, ?, CURRENT_TIMESTAMP
        )
        """,
        (
            "update_ticket_status",
            f"{ticket_id}:{new_status}",
            "SUCCESS",
            "SUCCESS"
        )
    )

    return {
        "ticket_id": ticket_id,
        "previous_status": current_status,
        "new_status": new_status
    }

@tool
def add_ticket_comment(ticket_id:str,comment:str):
    """
    Add Internal Ticket Comment.
    """
    ticket = fetching_one(
        """
        SELECT ticket_id
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )
    if not ticket:

        return {
            "error": f"Ticket {ticket_id} not found"
        }

    execution_query(
        """
        INSERT INTO ticket_comments
        (
            ticket_id,
            comment,
            created_at
        )
        VALUES
        (
            ?, ?, CURRENT_TIMESTAMP
        )
        """,
        (
            ticket_id,
            comment
        )
    )

    execution_query(
        """
        INSERT INTO tool_audit_logs
        (
            tool_name,
            input,
            output,
            status,
            created_at
        )
        VALUES
        (
            ?, ?, ?, ?, CURRENT_TIMESTAMP
        )
        """,
        (
            "add_ticket_comment",
            ticket_id,
            "SUCCESS",
            "SUCCESS"
        )
    )

    return {
        "success": True,
        "ticket_id": ticket_id
    }

@tool
def save_conversation_tool(session_id:str,user_message:str,agent_response:str,tools_used:str):
    """
    Save Conversation into memory.
    """
    result = saving_converstation(
        session_id=session_id,
        user_message=user_message,
        agent_response=agent_response,
        tools_used=tools_used
    )
    return result


@tool
def recall_conversation_tool(keyword: str):
    """
    Recall previous conversations.
    """
    conversations = recalling_coversation(keyword)

    return {
        "count": len(conversations),
        "results": conversations
    }

@tool
def save_archival_memory_tool(memory_key: str,memory_value: str,memory_type: str,importance: int):
    """
    Save long-term memory.
    """
    
    result = saving_archival_memory(
        memory_key=memory_key,
        memory_value=memory_value,
        memory_type=memory_type,
        importance=importance
    )

    execution_query(
        """
        INSERT INTO tool_audit_logs
        (
            tool_name,
            input,
            output,
            status,
            created_at
        )
        VALUES
        (
            ?, ?, ?, ?, CURRENT_TIMESTAMP
        )
        """,
        (
            "save_archival_memory",
            memory_key,
            "SUCCESS",
            "SUCCESS"
        )
    )
    return result

@tool
def recall_archival_memory_tool():
    """
    Recall saved preferences and rules.
    """
    memories = recall_archival_memory()
    return {
        "count": len(memories),
        "memories": memories
    }

@tool
def summarize_conversation(session_id: str):
    """
    Summarize recent conversation history.
    """
    conversations = getting_recent_conversation(
        session_id
    )

    if not conversations:
        return {
            "error": "No conversations found"
        }

    summary = f"{len(conversations)} conversation records found."
    key_decisions = "N/A"
    open_items = "N/A"

    saving_conversation_summary(
        session_id=session_id,
        summary=summary,
        key_decisions=key_decisions,
        open_items=open_items
    )

    execution_query(
        """
        INSERT INTO tool_audit_logs
        (
            tool_name,
            input,
            output,
            status,
            created_at
        )
        VALUES
        (
            ?, ?, ?, ?, CURRENT_TIMESTAMP
        )
        """,
        (
            "summarize_conversation",
            session_id,
            "SUCCESS",
            "SUCCESS"
        )
    )
    return {
        "summary": summary,
        "key_decisions": key_decisions,
        "open_items": open_items,
        "stored": True
    }


def get_tools():
    """
    Return all tools for the LangChain agent.
    """
    return [
        search_tickets,
        get_ticket_details,
        get_ticket_comments,
        calculate_sla_status,
        prioritize_tickets,
        update_ticket_status,
        add_ticket_comment,
        save_conversation_tool,
        recall_conversation_tool,
        save_archival_memory_tool,
        recall_archival_memory_tool,
        summarize_conversation
    ]

