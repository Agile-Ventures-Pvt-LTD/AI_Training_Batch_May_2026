import json
from typing import Optional
from langchain_core.tools import tool

import db_utils
import retrievers as ret_module


_vector_store = None


def get_vector_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = ret_module.load_vector_store()
    return _vector_store


@tool
def inspect_database_schema() -> str:
    """Inspect the IT support database to see all available tables and their columns. Call this first if unsure what data is available."""
    result = db_utils.inspect_schema()
    return json.dumps(result, indent=2)


@tool
def classify_issue_type(query: str) -> str:
    """Classify an IT support query into one of: VPN, OUTLOOK_EMAIL, LAPTOP_PERFORMANCE, PASSWORD_RESET, NETWORK_CONNECTIVITY, PRINTER, or UNKNOWN. Returns issue type and confidence."""
    issue_keywords = {
        "VPN": ["vpn", "virtual private network", "vpn timeout", "vpn disconnect", "vpn client", "tunnel"],
        "OUTLOOK_EMAIL": ["outlook", "email", "mail", "exchange", "inbox", "outbox", "mailbox", "sync email", "email not syncing"],
        "LAPTOP_PERFORMANCE": ["slow laptop", "laptop slow", "slow startup", "high cpu", "disk full", "memory usage", "laptop performance", "boot slow"],
        "PASSWORD_RESET": ["password", "login", "account locked", "cannot login", "reset password", "mfa", "authentication failed", "access denied", "locked out"],
        "NETWORK_CONNECTIVITY": ["internet", "network", "wifi", "wi-fi", "connectivity", "cannot connect", "network slow", "dns"],
        "PRINTER": ["printer", "print", "printing", "print queue", "printer offline", "stuck print"],
    }

    query_lower = query.lower()
    scores = {k: sum(1 for kw in v if kw in query_lower) for k, v in issue_keywords.items()}
    best = max(scores, key=scores.get)
    score = scores[best]

    if score == 0:
        issue_type, confidence = "UNKNOWN", "LOW"
    elif score == 1:
        issue_type, confidence = best, "MEDIUM"
    else:
        issue_type, confidence = best, "HIGH"

    return json.dumps(
        {
            "issue_type": issue_type,
            "confidence": confidence,
            "requires_device_lookup": issue_type in ["LAPTOP_PERFORMANCE", "VPN", "NETWORK_CONNECTIVITY"],
            "requires_incident_check": issue_type in ["VPN", "OUTLOOK_EMAIL", "NETWORK_CONNECTIVITY"],
        },
        indent=2,
    )


@tool
def retrieve_troubleshooting_steps(issue_type: str, query: str) -> str:
    """Retrieve relevant troubleshooting guidance from the IT knowledge base. Provide the classified issue type and original user query."""
    try:
        vs = get_vector_store()
        docs = ret_module.retrieve_by_issue_type(issue_type, query, vector_store=vs)
        chunks = ret_module.format_retrieved_chunks(docs)
        return json.dumps({"issue_type": issue_type, "chunks": chunks}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "chunks": []})


@tool
def get_user_profile(identifier: str) -> str:
    """Get user profile by full name, email address, or user ID (e.g. USR-1001). Returns department, location, account status, and MFA status."""
    try:
        identifier = identifier.strip()
        if identifier.upper().startswith("USR-"):
            user = db_utils.query_user_by_id(identifier.upper())
        elif "@" in identifier:
            user = db_utils.query_user_by_email(identifier)
        else:
            user = db_utils.query_user_by_name(identifier)

        if user:
            return json.dumps({"found": True, "user": user}, indent=2)
        return json.dumps({"found": False, "message": f"No user found for: {identifier}"})
    except Exception as e:
        return json.dumps({"found": False, "error": str(e)})


@tool
def get_device_status(user_id: str) -> str:
    """Get device health and compliance details for a user ID. Returns OS, compliance status, VPN client version, disk space, CPU, and memory usage."""
    try:
        device = db_utils.query_device_by_user_id(user_id.strip().upper())
        if device:
            return json.dumps({"found": True, "device": device}, indent=2)
        return json.dumps({"found": False, "message": f"No device found for: {user_id}"})
    except Exception as e:
        return json.dumps({"found": False, "error": str(e)})


@tool
def check_known_incidents(service_name: Optional[str] = None, region: Optional[str] = None, status: Optional[str] = "Active") -> str:
    """Check known IT incidents filtered by service name and region. Status defaults to Active. Services include VPN Gateway, Email Exchange, Active Directory, Network."""
    try:
        incidents = db_utils.query_known_incidents(service_name=service_name, region=region, status=status)
        return json.dumps({"count": len(incidents), "incidents": incidents}, indent=2)
    except Exception as e:
        return json.dumps({"count": 0, "incidents": [], "error": str(e)})


@tool
def run_diagnostic_check(user_id: str) -> str:
    """Get the latest diagnostic snapshot for a user ID. Shows VPN reachability, internet status, webmail, internal apps, mailbox quota, account lock, and MFA push result."""
    try:
        snapshot = db_utils.query_diagnostic_snapshot(user_id.strip().upper())
        if snapshot:
            return json.dumps({"found": True, "snapshot": snapshot}, indent=2)
        return json.dumps({"found": False, "message": f"No diagnostic snapshot found for: {user_id}"})
    except Exception as e:
        return json.dumps({"found": False, "error": str(e)})


@tool
def get_ticket_details(ticket_id: Optional[str] = None, user_id: Optional[str] = None) -> str:
    """Get IT support ticket(s) by ticket ID (e.g. IT-3001) or by user ID. Returns issue type, priority, status, subject, and assigned support group."""
    try:
        if ticket_id:
            ticket = db_utils.query_ticket_by_id(ticket_id.strip().upper())
            if ticket:
                return json.dumps({"found": True, "ticket": ticket}, indent=2)
            return json.dumps({"found": False, "message": f"No ticket found: {ticket_id}"})
        elif user_id:
            tickets = db_utils.query_tickets_by_user_id(user_id.strip().upper())
            return json.dumps({"found": len(tickets) > 0, "count": len(tickets), "tickets": tickets}, indent=2)
        return json.dumps({"found": False, "message": "Provide ticket_id or user_id."})
    except Exception as e:
        return json.dumps({"found": False, "error": str(e)})


@tool
def search_tickets(keyword: Optional[str] = None, issue_type: Optional[str] = None, status: Optional[str] = None) -> str:
    """Search IT support tickets by keyword in subject or description, issue type, or status (Open/Closed). Useful for finding related or duplicate tickets."""
    try:
        tickets = db_utils.search_tickets(keyword=keyword, issue_type=issue_type, status=status)
        return json.dumps({"count": len(tickets), "tickets": tickets}, indent=2)
    except Exception as e:
        return json.dumps({"count": 0, "tickets": [], "error": str(e)})


@tool
def get_active_incidents() -> str:
    """Get all currently active IT incidents across all services and regions. Use this to check for widespread outages affecting multiple users."""
    try:
        incidents = db_utils.get_all_active_incidents()
        return json.dumps({"count": len(incidents), "incidents": incidents}, indent=2)
    except Exception as e:
        return json.dumps({"count": 0, "incidents": [], "error": str(e)})
