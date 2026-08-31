from langchain.tools import tool
import db_utils
import retrievers
from vector_store import load_vector_store

def retrieve_troubleshooting_steps(issue_type: str, query: str):
    """
    Retrieve troubleshooting guidance from knowledge base.
    Returns relevant guide sections for the issue.
    Args:
        issue_type: Type of issue (VPN, OUTLOOK_EMAIL, LAPTOP_PERFORMANCE, etc.)
        query: Specific question or symptom to search for
    Returns:
        Dictionary with issue_type and list of relevant chunks
    """
    vector_store = load_vector_store()
    if not vector_store:
        return {"error": "Knowledge base not initialized"}
    retriever = retrievers.create_rag_retriever(vector_store)
    results = retrievers.retrieve_troubleshooting(retriever, query, issue_type)

    return {
        "issue_type": issue_type,
        "query": query,
        "chunks_found": len(results),
        "chunks": results
    }


def get_user_profile(user_identifier: str):
    """
    Retrieve user profile information.
    Search by user ID or full name.
    Args:
        user_identifier: User ID or name to search
    Returns:
        Dictionary with user details or error message
    """
    user = db_utils.get_user_profile(user_identifier)
    if user:
        return {
            "found": True,
            "user": user
        }
    else:
        return {
            "found": False,
            "error": f"User not found: {user_identifier}"
        }

def get_device_status(user_id: str):
    """
    Get device metrics and status for a user.
    Shows performance and compliance information.
    Args:
        user_id: The user's ID
    Returns:
        Dictionary with device details or error
    """
    device = db_utils.get_device_status(user_id)
    if device:
        return {
            "found": True,
            "device": device
        }
    else:
        return {
            "found": False,
            "error": f"Device not found for user: {user_id}"
        }


def check_known_incidents(service_name: str = None):
    """
    Retrieve active known incidents that may affect resolution.
    Args:
        service_name: Optional service to filter incidents (VPN, EMAIL, etc.)
    Returns:
        Dictionary with count and list of incidents
    """
    incidents = db_utils.check_known_incidents(service_name)
    return {
        "filter": service_name,
        "count": len(incidents),
        "incidents": incidents
    }


def run_diagnostic_check(user_id: str):
    """
    Get diagnostic snapshot showing user's connectivity and service status.
    Args:
        user_id: The user's ID
    Returns:
        Dictionary with diagnostic results or error
    """
    diagnostics = db_utils.get_diagnostic_snapshot(user_id)
    if diagnostics:
        return {
            "found": True,
            "diagnostics": diagnostics
        }
    else:
        return {
            "found": False,
            "error": f"No diagnostics found for user: {user_id}"
        }


def get_ticket_details(ticket_id: str):
    """
    Retrieve details of an existing support ticket.
    Args:
        ticket_id: The ticket ID to look up
    Returns:
        Dictionary with ticket information or error
    """
    ticket = db_utils.get_ticket_details(ticket_id)
    if ticket:
        return {
            "found": True,
            "ticket": ticket
        }
    else:
        return {
            "found": False,
            "error": f"Ticket not found: {ticket_id}"
        }


def create_resolution_plan(issue_type: str, user_data: dict, device_data: dict):
    """
    Create a diagnostic summary and resolution plan based on gathered data.
    Args:
        issue_type: Classified issue type
        user_data: User profile information
        device_data: Device metrics and status
    Returns:
        Dictionary with diagnosis, recommended steps, and escalation flag
    """
    device = device_data.get("device", {})
    risk_signals = []
    if device.get("compliance_status") == "FAILED":
        risk_signals.append("Device not compliant")
    if device.get("cpu_usage_percent", 0) > 80:
        risk_signals.append("High CPU usage")
    if device.get("memory_usage_percent", 0) > 85:
        risk_signals.append("High memory usage")
    if device.get("disk_free_percent", 0) < 5:
        risk_signals.append("Low disk space")
    
    escalation_required = len(risk_signals) > 0 or issue_type == "PASSWORD_RESET"
    
    escalation_group = "Endpoint Support"
    if issue_type == "PASSWORD_RESET":
        escalation_group = "Identity Access Management"
    elif issue_type == "VPN":
        escalation_group = "Network Support"
    elif issue_type == "OUTLOOK_EMAIL":
        escalation_group = "Messaging Support"
    return {
        "issue_type": issue_type,
        "diagnosis_summary": f"Analyzing {issue_type} issue",
        "risk_signals": risk_signals,
        "recommended_steps": [
            "Verify user identity",
            "Check device status",
            "Review knowledge base",
            "Test connectivity" if issue_type == "VPN" else "Check service status"
        ],
        "escalation_required": escalation_required,
        "escalation_group": escalation_group,
        "safety_notes": [
            "Do not request sensitive credentials",
            "Verify device compliance before troubleshooting",
            "Document all steps taken"
        ],
        "confidence": "HIGH" if len(risk_signals) == 0 else "MEDIUM"
    }


def get_all_tools():
    return [
        retrieve_troubleshooting_steps,
        get_user_profile,
        get_device_status,
        check_known_incidents,
        run_diagnostic_check,
        get_ticket_details,
        create_resolution_plan
    ]
