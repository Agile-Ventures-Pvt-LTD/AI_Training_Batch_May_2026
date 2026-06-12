from langchain_core.tools import tool

from db_utils import (
    fetch_all,
    fetch_one,
    execute_query
)

from memory import (
    save_conversation,
    recall_conversation,
    save_archival_memory,
    recall_archival_memory,
    save_summary
)

from datetime import datetime


def log_tool_action(
        tool_name,
        input_data,
        output,
        status="SUCCESS"
):

    query = """

    INSERT INTO tool_audit_logs
    (
    tool_name,
    input,
    output,
    status,
    created_at
    )

    VALUES (?,?,?,?,?)

    """


    execute_query(
        query,
        (
            tool_name,
            str(input_data),
            str(output),
            status,
            datetime.now().isoformat()
        )
    )




@tool
def search_tickets(
    status=None,
    priority=None,
    category=None,
    customer_tier=None,
    overdue_only=False,
    keyword=None
):
    """
    Search helpdesk tickets using filters.
    """

    query = """

    SELECT 
    t.ticket_id,
    t.subject,
    t.priority,
    t.status,
    t.category,
    t.due_at,
    c.customer_tier

    FROM tickets t

    LEFT JOIN customers c
    ON t.customer_id=c.customer_id

    WHERE 1=1

    LIMIT 20
    """


    params=[]


    if status:
        query += " AND t.status=? "
        params.append(status)


    if priority:
        query += " AND t.priority=? "
        params.append(priority)


    if category:
        query += " AND t.category=? "
        params.append(category)


    if customer_tier:
        query += " AND c.customer_tier=? "
        params.append(customer_tier)


    if keyword:

        query += """
        AND
        (
        t.subject LIKE ?
        OR
        t.description LIKE ?
        )
        """

        params.extend(
            [
                f"%{keyword}%",
                f"%{keyword}%"
            ]
        )


    if overdue_only:

        query += """

        AND date(t.due_at)<date('now')
        AND t.status NOT IN ('Closed','Resolved')

        """



    result = fetch_all(
        query,
        tuple(params)
    )


    return {
    "count": len(result),
    "tickets": result
}


@tool
def get_ticket_details(ticket_id:str):
    """
    Fetch complete ticket information.
    """

    query="""

    SELECT

    t.*,
    c.customer_name,
    c.company_name,
    c.customer_tier

    FROM tickets t

    LEFT JOIN customers c

    ON t.customer_id=c.customer_id

    WHERE t.ticket_id=?

    """


    result = fetch_one(
        query,
        (ticket_id,)
    )


    if not result:

        return {
            "error":
            "Ticket not found"
        }


    return result




@tool
def get_ticket_comments(ticket_id:str):
    """
    Fetch ticket history and work notes.
    """


    query="""

    SELECT *

    FROM ticket_comments

    WHERE ticket_id=?

    ORDER BY created_at

    """


    return fetch_all(
        query,
        (ticket_id,)
    )




@tool
def calculate_sla_status(ticket_id:str):
    """
    Calculate SLA status of ticket.
    """


    query="""

    SELECT
    ticket_id,
    status,
    due_at

    FROM tickets

    WHERE ticket_id=?

    """

    ticket = fetch_one(
        query,
        (ticket_id,)
    )


    if not ticket:

        return {
            "error":
            "Ticket not found"
        }



    due_date = ticket["due_at"]

    today=datetime.now().date()



    if ticket["status"] in [
        "Closed",
        "Resolved"
    ]:

        sla="WITHIN_SLA"



    elif str(due_date)<str(today):

        sla="BREACHED"



    elif str(due_date)==str(today):

        sla="DUE_TODAY"


    else:

        sla="WITHIN_SLA"



    return {

        "ticket_id":ticket_id,
        "sla_status":sla,
        "due_at":due_date,
        "status":ticket["status"]

    }


@tool
def prioritize_tickets():
    """
    Rank tickets based on priority, SLA risk, and customer importance.
    """

    result = search_tickets.invoke(
        {
            "status": "Open"
        }
    )


    if isinstance(result, str):

        return {
            "error": result
        }


    if isinstance(result, str):

        return {
            "message": result
        }


    if not isinstance(result, dict):

        return {
            "message": "Unexpected tool response format"
        }


    tickets = result.get(
    "tickets",
    []
)


    if not tickets:

        return {
            "message":
            "No open tickets found"
        }



    prioritized = []


    for ticket in tickets:


        score = 0

        reasons = []



        if ticket.get("priority") == "Urgent":

            score += 50

            reasons.append(
                "Urgent priority"
            )


        elif ticket.get("priority") == "High":

            score += 30

            reasons.append(
                "High priority"
            )



        if ticket.get("customer_tier") == "Enterprise":

            score += 20

            reasons.append(
                "Enterprise customer"
            )



        sla_result = calculate_sla_status.invoke(

            {
                "ticket_id":
                ticket.get("ticket_id")
            }

        )


        if isinstance(
            sla_result,
            dict
        ):


            if sla_result.get(
                "sla_status"
            ) == "BREACHED":


                score += 40

                reasons.append(
                    "SLA breached"
                )



        prioritized.append(

            {

                "ticket_id":
                ticket.get("ticket_id"),


                "subject":
                ticket.get("subject"),


                "priority":
                ticket.get("priority"),


                "status":
                ticket.get("status"),


                "score":
                score,


                "reason":
                reasons

            }

        )



    prioritized.sort(

        key=lambda x:x["score"],

        reverse=True

    )


    return {

        "recommended_order":
        prioritized

    }


@tool
def update_ticket_status(
        ticket_id:str,
        new_status:str
):
    """
    Safely update ticket status.
    """


    allowed=[
        "Open",
        "In Progress",
        "Pending",
        "Resolved",
        "Closed",
        "Escalated"
    ]


    if new_status not in allowed:

        return {
            "error":
            "Invalid status"
        }



    ticket=get_ticket_details.invoke(
        {
            "ticket_id":
            ticket_id
        }
    )


    if "error" in ticket:

        return ticket



    old_status=ticket["status"]



    if old_status==new_status:

        return {
            "message":
            "Ticket already has this status"
        }



    query="""

    UPDATE tickets

    SET status=?

    WHERE ticket_id=?

    """



    execute_query(
        query,
        (
            new_status,
            ticket_id
        )
    )


    result={

        "ticket_id":ticket_id,

        "old_status":
        old_status,

        "new_status":
        new_status,

        "message":
        "Status updated successfully"

    }


    log_tool_action(
        "update_ticket_status",
        {
            "ticket_id":ticket_id,
            "new_status":new_status
        },
        result
    )


    return result


@tool
def add_ticket_comment(
        ticket_id:str,
        comment:str
):
    """
    Add internal ticket work note.
    """



    ticket=get_ticket_details.invoke(
        {
            "ticket_id":
            ticket_id
        }
    )


    if "error" in ticket:

        return ticket



    query="""

    INSERT INTO ticket_comments

    (
    ticket_id,
    comment,
    created_at
    )

    VALUES (?,?,?)

    """



    execute_query(
        query,
        (
            ticket_id,
            comment,
            datetime.now().isoformat()
        )
    )


    result={
        "message":
        "Comment added successfully"
    }


    log_tool_action(
        "add_ticket_comment",
        {
            "ticket_id":ticket_id,
            "comment":comment
        },
        result
    )


    return result




@tool
def save_conversation_tool(
        session_id: str,
        user_message: str,
        agent_response: str,
        tools_used: str
):
    """
    Save current conversation between user and AI agent.
    """

    return save_conversation(
        session_id,
        user_message,
        agent_response,
        tools_used
    )



@tool
def recall_conversation_tool(
        keyword: str
):

    """
    Search previous conversations using a keyword.
    """

    result = recall_conversation(
        keyword
    )


    if isinstance(result, str):

        return {
            "conversation": result
        }


    return {
        "conversation": result
    }


@tool
def save_archival_memory_tool(
        memory_key: str,
        memory_value: str
):
    """
    Store permanent user preferences in archival memory.
    """

    return save_archival_memory(
        memory_key,
        memory_value
    )



@tool
def recall_archival_memory_tool():

    """
    Retrieve saved user preferences and memories.
    """

    result = recall_archival_memory()


    if isinstance(result, str):

        return {
            "memory": result
        }


    return {
        "memory": result
    }


@tool
def summarize_conversation_tool(
        session_id: str,
        summary: str,
        decisions: str,
        open_items: str
):
    """
    Store summarized conversation information.
    """

    return save_summary(
        session_id,
        summary,
        decisions,
        open_items
    )


TOOLS=[

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

    summarize_conversation_tool

]