import json
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
from db_utils import DatabaseManager
from loaders import load_vector_store
from retrievers import Retriever

db = DatabaseManager()
vector_store = load_vector_store()
retriever = Retriever(vector_store)

@tool
def retrieve_troubleshooting_steps(issue_type: str, query: str) -> str:
    """
    Retrieve relevant troubleshooting guidance snippets from the knowledge base.
    Input parameters:
      issue_type: The classified issue category like VPN,Email.
      query: It is a specific descriptions or user error statements.
    """
    if not retriever:
        return json.dumps({"error": "Vector store does not initialized correctly."})
    
    retrieve = retriever.retrieve_troubleshooting_steps(issue_type=issue_type, query=query)

    return json.dumps(retrieve, indent=2)

@tool 
def get_user_profile(user_id:str, full_name:str, email:str) -> str:
    """
    Fetch user informations from the internal database (sqlite) by using user_id, full_name, or email.
    """
    query = """
        select user_id, full_name, department, location, account_status, mfa_status 
        from users 
        where (? IS NOT NULL AND user_id = ?)
           or (? IS NOT NULL AND full_name LIKE ?)
           or (? IS NOT NULL AND email = ?)
    """
    rows = db.execute_sql_query(query, (user_id, user_id,full_name,full_name,email, email))
    
    if rows:
        return json.dumps({"found": True, "user": rows[0]}, indent=2)
    return json.dumps({"found": False, "message": "No matching user record found."}, indent=2)

@tool
def get_device_status(user_id: str) -> str:
    """
    Fetch device health and compliances details for a given user_id.
    """
    query = """
        select user_id, device_id, compliance_status, vpn_client_version, disk_free_percent, cpu_usage_percent, memory_usage_percent 
        from devices 
        where user_id = ?
    """
    rows = db.execute_sql_query(query, (user_id,))
    if rows:
        return json.dumps(rows[0], indent=2)
    return json.dumps({"error": f"No such active registered devices found for user {user_id}."}, indent=2)

@tool
def check_known_incidents(service_name: str,status:str) -> str:
    """
    Check for active incidents by service name, region or keyword name.
    """
    query = """
        select incident_id, service_name, region, severity, status, summary, workaround 
        from known_incidents 
        where service_name LIKE ? AND status = 'Active'
    """
    rows = db.execute_sql_query(query, (service_name,status))
    return json.dumps({"count": len(rows), "incidents": rows}, indent=2)

@tool
def run_diagnostic_check(user_id: str) -> str:
    """
    Run diagnostic snapshots for a given user_id and device.
    """
    query = """
        select user_id, vpn_reachable, internet_reachable, webmail_reachable, internal_apps_reachable, account_locked, mfa_push_success 
        from diagnostic_snapshots 
        where user_id = ?
    """
    rows = db.execute_sql_query(query, (user_id,))
    if rows:
        first_row = rows[0]
        boolean = {
            k: (bool(v) if any(x in k for x in ["reachable", "locked", "success"]) else v) 
            for k, v in first_row.items()
        }
        return json.dumps(boolean, indent=2)
    return json.dumps({"error": f"Diagnostic generation failed for user {user_id}."}, indent=2)

@tool
def get_ticket_details(ticket_id: str) -> str:
    """
    Fetch existing IT support ticket details.
    """
    query = """
        select ticket_id, user_id, issue_type, priority, status, subject, assigned_group 
        from tickets 
        where ticket_id = ?
    """
    rows = db.execute_sql_query(query, (ticket_id,))
    if rows:
        return json.dumps(rows[0], indent=2)
    return json.dumps({"error": f"Ticket {ticket_id} could not be resolved or found."}, indent=2)

@tool
def generate_resolution_plan(diagnosis_summary: str,recommended_steps: List[str],escalation_required: bool,escalation_group: str,safety_notes: List[str],confidence: str) -> str:
    """
    Submit the final synthesized resolution plan for the user issue.
    Args:
        diagnosis_summary: Detailed technical diagnosis based on evidence.
        recommended_steps: Ordered list of text steps to resolve the issue.
        escalation_required: True if it needs escalation,otherwise False.
        escalation_group: Choose from: Identity Access Management, Network Support, Messaging Support, Endpoint Support, Workplace IT. Empty string if false.
        safety_notes: Critical security guardrails or standard IT safety notices.
        confidence: Must be strictly one of these values: HIGH, MEDIUM, LOW.
    """
    plan_output = {
        "diagnosis_summary": diagnosis_summary,
        "recommended_steps": recommended_steps,
        "escalation_required": escalation_required,
        "escalation_group": escalation_group,
        "safety_notes": safety_notes,
        "confidence": confidence
    }
    
    return json.dumps(plan_output, indent=2)

Tools = [retrieve_troubleshooting_steps,get_user_profile,get_device_status,check_known_incidents, run_diagnostic_check,get_ticket_details]