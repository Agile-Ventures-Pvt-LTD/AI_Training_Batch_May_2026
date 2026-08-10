from langchain_core.tools import tool
from db_utils import fetch_one, fetch_all, execute_write
from langchain_groq import ChatGroq
from datetime import datetime
from config import llm
import os

@tool
def get_ticket_details(ticket_id: str = "") -> dict:
    """
    Fetch complete details for a single ticket.

    Input:
        ticket_id: Ticket identifier (e.g., TCK-1003)

    Output:
    {
        "ticket_id": "",
        "customer_name": "",
        "company_name": "",
        "customer_tier": "",
        "category": "",
        "priority": "",
        "status": "",
        "subject": "",
        "description": "",
        "created_date": "",
        "due_date": "",
        "assigned_agent": ""
    }
    """

    query = "SELECT * FROM tickets WHERE ticket_id = ?"
    result = fetch_one(query, (ticket_id,))

    if not result:
        return {"error": "Ticket not found"}

    return {
        "ticket_id": result.get("ticket_id"),
        "customer_name": result.get("customer_name"),
        "company_name": result.get("company_name"),
        "customer_tier": result.get("customer_tier"),
        "category": result.get("category"),
        "priority": result.get("priority"),
        "status": result.get("status"),
        "subject": result.get("subject"),
        "description": result.get("description"),
        "created_date": result.get("created_date"),
        "due_date": result.get("due_date"),
        "assigned_agent": result.get("assigned_agent")
    }

#================================================================

@tool
def get_ticket_details(ticket_id: str = "") -> dict:
    """
    Fetch complete details for a single ticket.

    Input:
        ticket_id: Ticket identifier (e.g., TCK-1003)

    Output:
    {
        "ticket_id": "",
        "customer_name": "",
        "company_name": "",
        "customer_tier": "",
        "category": "",
        "priority": "",
        "status": "",
        "subject": "",
        "description": "",
        "created_date": "",
        "due_date": "",
        "assigned_agent": ""
    }
    """

    query = "SELECT * FROM tickets WHERE ticket_id = ?"
    result = fetch_one(query, (ticket_id,))

    if not result:
        return {"error": "Ticket not found"}

    return {
        "ticket_id": result.get("ticket_id"),
        "customer_name": result.get("customer_name"),
        "company_name": result.get("company_name"),
        "customer_tier": result.get("customer_tier"),
        "category": result.get("category"),
        "priority": result.get("priority"),
        "status": result.get("status"),
        "subject": result.get("subject"),
        "description": result.get("description"),
        "created_date": result.get("created_date"),
        "due_date": result.get("due_date"),
        "assigned_agent": result.get("assigned_agent")
    }

#================================================================

@tool
def get_ticket_comments(ticket_id: str= "") -> dict:
    """
    Fetch ticket history or work notes for a given ticket ID.

    Input:
        ticket_id: Ticket identifier (e.g., TCK-1001)

    Output:
    {
        "ticket_id": "",
        "count": 2,
        "comments": [
            {
                "comment": "",
                "created_at": "",
                "author": ""
            }
        ]
    }
    """

    query = """
        SELECT ticket_id, comment, created_at, author
        FROM ticket_comments
        WHERE ticket_id = ?
        ORDER BY created_at ASC
    """

    rows = fetch_all(query, (ticket_id,))

    if not rows:
        return {
            "ticket_id": ticket_id,
            "count": 0,
            "comments": []
        }

    return {
        "ticket_id": ticket_id,
        "count": len(rows),
        "comments": [
            {
                "comment": r.get("comment"),
                "created_at": r.get("created_at"),
                "author": r.get("author")
            }
            for r in rows
        ]
    }

#================================================================

@tool
def calculate_sla_status(ticket_id: str= "") -> dict:
    """
    Determine whether a ticket is:
    - BREACHED
    - DUE_TODAY
    - WITHIN_SLA

    Input:
        ticket_id: Ticket identifier (e.g., TCK-1003)

    Output:
    {
        "ticket_id": "",
        "sla_status": "BREACHED | DUE_TODAY | WITHIN_SLA",
        "due_at": "",
        "status": "",
        "reason": ""
    }
    """

    query = "SELECT status, due_at FROM tickets WHERE ticket_id = ?"
    result = fetch_one(query, (ticket_id,))

    if not result:
        return {
            "ticket_id": ticket_id,
            "sla_status": "UNKNOWN",
            "due_at": None,
            "status": None,
            "reason": "Ticket not found"
        }

    due_at = result.get("due_at")
    status = result.get("status")

    if not due_at:
        return {
            "ticket_id": ticket_id,
            "sla_status": "UNKNOWN",
            "due_at": None,
            "status": status,
            "reason": "No due date available"
        }

    today = date.today()
    due_date = datetime.strptime(due_at, "%Y-%m-%d").date()

    # ---------------- SLA LOGIC ----------------
    if status in ["Closed", "Resolved"]:
        sla_status = "WITHIN_SLA"
        reason = "Ticket already resolved/closed"

    elif due_date < today:
        sla_status = "BREACHED"
        reason = "Due date has passed"

    elif due_date == today:
        sla_status = "DUE_TODAY"
        reason = "Due today"

    else:
        sla_status = "WITHIN_SLA"
        reason = "Still within SLA window"

    return {
        "ticket_id": ticket_id,
        "sla_status": sla_status,
        "due_at": due_at,
        "status": status,
        "reason": reason
    }
from datetime import datetime, date
#================================================================

@tool
def prioritize_tickets() -> dict:
    """
    Rank tickets based on:
    - Priority
    - SLA status
    - Customer tier
    - Ticket status
    - Business rules (Enterprise priority boost)

    Output:
    {
        "ranked_tickets": [
            {
                "ticket_id": "",
                "priority_score": 0,
                "reason": ""
            }
        ],
        "summary": ""
    }
    """

    query = """
        SELECT ticket_id, subject, priority, status, customer_tier, due_at
        FROM tickets
        WHERE status != 'Closed'
    """

    tickets = fetch_all(query)

    ranked = []

    today = datetime.now().date()

    for t in tickets:
        score = 0
        reasons = []

        # Priority scoring
        if t["priority"] == "Urgent":
            score += 50
            reasons.append("Urgent priority")
        elif t["priority"] == "High":
            score += 30
            reasons.append("High priority")
        else:
            score += 10

        # Customer tier boost
        if t["customer_tier"] == "Enterprise":
            score += 40
            reasons.append("Enterprise customer")

        # SLA logic (simple inline version)
        if t["due_at"]:
            due_date = datetime.strptime(t["due_at"], "%Y-%m-%d").date()

            if due_date < today:
                score += 60
                reasons.append("SLA BREACHED")
            elif due_date == today:
                score += 40
                reasons.append("Due today")

        # Business category boost
        if "billing" in (t["subject"] or "").lower():
            score += 15
            reasons.append("Billing issue")

        ranked.append({
            "ticket_id": t["ticket_id"],
            "subject": t["subject"],
            "priority_score": score,
            "reason": ", ".join(reasons)
        })

    # Sort by score
    ranked.sort(key=lambda x: x["priority_score"], reverse=True)

    return {
        "ranked_tickets": ranked[:5],
        "summary": "Tickets ranked using priority, SLA, customer tier, and business rules."
    }

#================================================================

@tool
def update_ticket_status(ticket_id: str = "", new_status: str = "") -> dict:
    """
    Update ticket status safely.

    Rules:
    - Validate ticket exists
    - Validate allowed status
    - Prevent duplicate update
    - Log all changes in tool_audit_logs

    Output:
    {
        "ticket_id": "",
        "old_status": "",
        "new_status": "",
        "updated": true/false,
        "message": ""
    }
    """

    allowed_statuses = ["Open", "In Progress", "Pending", "Resolved", "Closed", "Escalated"]

    # 1. Fetch ticket
    ticket = fetch_one(
        "SELECT status FROM tickets WHERE ticket_id = ?",
        (ticket_id,)
    )

    if not ticket:
        return {
            "ticket_id": ticket_id,
            "updated": False,
            "message": "Ticket not found"
        }

    current_status = ticket["status"]

    # 2. Validate status
    if new_status not in allowed_statuses:
        return {
            "ticket_id": ticket_id,
            "updated": False,
            "message": f"Invalid status. Allowed: {allowed_statuses}"
        }

    # 3. No change needed
    if current_status == new_status:
        return {
            "ticket_id": ticket_id,
            "updated": False,
            "message": f"Ticket already in {new_status}"
        }

    # 4. Update ticket
    execute_write(
        "UPDATE tickets SET status = ? WHERE ticket_id = ?",
        (new_status, ticket_id)
    )

    # 5. Audit log (FR-15 requirement)
    execute_write(
        """
        INSERT INTO tool_audit_logs (tool_name, input, output, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            "update_ticket_status",
            str({"ticket_id": ticket_id, "new_status": new_status}),
            str({"old_status": current_status, "new_status": new_status}),
            "SUCCESS",
            datetime.now().isoformat()
        )
    )

    return {
        "ticket_id": ticket_id,
        "old_status": current_status,
        "new_status": new_status,
        "updated": True,
        "message": f"Updated {ticket_id} from {current_status} to {new_status}"
    }
from db_utils import fetch_one, execute_write, fetch_all

#================================================================

@tool
def add_ticket_comment(ticket_id: str ="", comment: str ="") -> dict:
    """
    Add an internal comment to a ticket.

    Input:
        ticket_id: Ticket ID (e.g., TCK-1001)
        comment: Work note or internal update

    Output:
    {
        "ticket_id": "",
        "comment_added": true,
        "message": ""
    }
    """

    # 1. Validate ticket exists
    ticket = fetch_one(
        "SELECT ticket_id FROM tickets WHERE ticket_id = ?",
        (ticket_id,)
    )

    if not ticket:
        return {
            "ticket_id": ticket_id,
            "comment_added": False,
            "message": "Ticket not found"
        }

    # 2. Insert comment
    execute_write(
        """
        INSERT INTO ticket_comments (ticket_id, comment, created_at)
        VALUES (?, ?, ?)
        """,
        (ticket_id, comment, datetime.now().isoformat())
    )

    # 3. Audit log (FR-15 requirement)
    execute_write(
        """
        INSERT INTO tool_audit_logs (tool_name, input, output, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            "add_ticket_comment",
            str({"ticket_id": ticket_id, "comment": comment}),
            str({"status": "comment_added"}),
            "SUCCESS",
            datetime.now().isoformat()
        )
    )

    return {
        "ticket_id": ticket_id,
        "comment_added": True,
        "message": f"Comment added to {ticket_id}"
    }

#================================================================

@tool
def save_conversation(data: dict) -> dict:
    """
    Save conversation logs into conversation_logs table.

    Input:
    {
        "session_id": "",
        "user_message": "",
        "agent_response": "",
        "tools_used": ""
    }

    Output:
    {
        "saved": true,
        "session_id": ""
    }
    """

    session_id = data.get("session_id")
    user_message = data.get("user_message")
    agent_response = data.get("agent_response")
    tools_used = data.get("tools_used", "")

    if not session_id or not user_message:
        return {
            "saved": False,
            "message": "session_id and user_message are required"
        }

    execute_write(
        """
        INSERT INTO conversation_logs
        (session_id, user_message, agent_response, tools_used, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            session_id,
            user_message,
            agent_response,
            tools_used,
            datetime.now().isoformat()
        )
    )

    return {
        "saved": True,
        "session_id": session_id
    }

#================================================================


@tool
def recall_conversation(session_id: str = None, keyword: str = None) -> dict:
    """
    Retrieve past conversations from conversation_logs.

    Supports:
    - session_id search
    - keyword search (LIKE)

    Output:
    {
        "count": 0,
        "conversations": [
            {
                "user_message": "",
                "agent_response": "",
                "tools_used": ""
            }
        ]
    }
    """

    query = "SELECT user_message, agent_response, tools_used FROM conversation_logs WHERE 1=1"
    params = []

    # session filter
    if session_id:
        query += " AND session_id = ?"
        params.append(session_id)

    # keyword filter (FR requirement)
    if keyword:
        query += " AND user_message LIKE ?"
        params.append(f"%{keyword}%")

    rows = fetch_all(query, params)

    if not rows:
        return {
            "count": 0,
            "conversations": []
        }

    return {
        "count": len(rows),
        "conversations": [
            {
                "user_message": r.get("user_message"),
                "agent_response": r.get("agent_response"),
                "tools_used": r.get("tools_used")
            }
            for r in rows
        ]
    }

#================================================================

@tool
def save_archival_memory(data: dict) -> dict:
    """
    Store long-term user preferences or business rules.

    Input:
    {
        "memory_key": "",
        "memory_value": "",
        "memory_type": "preference | rule | note",
        "importance": 1-5
    }

    Output:
    {
        "saved": true,
        "memory_key": ""
    }
    """

    memory_key = data.get("memory_key")
    memory_value = data.get("memory_value")
    memory_type = data.get("memory_type", "preference")
    importance = data.get("importance", 3)

    if not memory_key or not memory_value:
        return {
            "saved": False,
            "message": "memory_key and memory_value are required"
        }

    execute_write(
        """
        INSERT INTO archival_memory
        (memory_key, memory_value, memory_type, importance, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            memory_key,
            memory_value,
            memory_type,
            importance,
            datetime.now().isoformat()
        )
    )

    return {
        "saved": True,
        "memory_key": memory_key
    }

#================================================================

@tool
def recall_archival_memory(memory_key: str = "") -> dict:
    """
    Retrieve long-term memory for decision making.

    Input:
        memory_key: key of stored memory

    Output:
    {
        "memory_key": "",
        "memory_value": "",
        "memory_type": "",
        "importance": 0
    }
    """

    query = """
        SELECT memory_key, memory_value, memory_type, importance
        FROM archival_memory
        WHERE memory_key = ?
    """

    result = fetch_one(query, (memory_key,))

    if not result:
        return {
            "found": False,
            "message": "No memory found"
        }

    return {
        "found": True,
        "memory_key": result.get("memory_key"),
        "memory_value": result.get("memory_value"),
        "memory_type": result.get("memory_type"),
        "importance": result.get("importance")
    }

#=================================================================

@tool
def summarize_conversation(session_id: str = "") -> dict:
    """
    Summarize conversation and store in conversation_summaries.

    Output:
    {
        "summary": "",
        "key_decisions": "",
        "open_items": "",
        "stored": true
    }
    """

    # 1. Fetch conversation logs
    logs = fetch_all(
        """
        SELECT user_message, agent_response
        FROM conversation_logs
        WHERE session_id = ?
        ORDER BY created_at DESC
        LIMIT 20
        """,
        (session_id,)
    )

    if not logs:
        return {
            "stored": False,
            "message": "No conversation found"
        }

    conversation_text = "\n".join(
        [f"User: {l['user_message']}\nAgent: {l['agent_response']}" for l in logs]
    )

    # 2. Groq prompt
    prompt = f"""
    You are a conversation summarizer.

    Extract:
    1. summary
    2. key decisions
    3. open items

    Conversation:
    {conversation_text}

    Return in JSON format:
    {{
        "summary": "",
        "key_decisions": "",
        "open_items": ""
    }}
    """

    response = llm.invoke(prompt)

    # Assume response.content is JSON string
    import json
    data = json.loads(response.content)

    # 3. Store in DB
    execute_write(
        """
        INSERT INTO conversation_summaries
        (session_id, summary, key_decisions, open_items, stored_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            session_id,
            data.get("summary"),
            data.get("key_decisions"),
            data.get("open_items"),
            datetime.now().isoformat()
        )
    )

    return {
        "summary": data.get("summary"),
        "key_decisions": data.get("key_decisions"),
        "open_items": data.get("open_items"),
        "stored": True
    }




