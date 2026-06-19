from langchain_core.tools import tool
from retrievers import retrieve_by_issue
from prompts import ISSUE_CLASSIFICATION,SYSTEM_PROMPT,TROUBLESHOOTING_RETERIVAL_TOOL,QUERY_REWRITE_PROMPT,ANSWER_PROMPT,REFLECTION_PROMPT
from config import GROQ_API_KEY,GROQ_MODEL
from langchain_groq import ChatGroq
from retrievers import retrieve_policies
from datetime import datetime, timedelta
from db_utils import execute_select_query
llm = ChatGroq(api_key=GROQ_API_KEY,model=GROQ_MODEL,temperature=0)
from output_parser import safe_json_parse

def retrieve_troubleshooting_steps(state):
    """Retrieve relevant troubleshooting guidance from the knowledge base."""
    question = state["user_question"]
    prompt = f"""{SYSTEM_PROMPT}
            Question:{question}"""
    response = llm.invoke(prompt)
    result = safe_json_parse(response.content)
    if not result:
        question_lower = question.lower()
        if "VPN" in question_lower:
            result = {"issue_type": "VPN","chunks": [{"source_file": "vpn_troubleshooting_guide.md","chunk_id": "vpn_chunk_002","snippet": "If VPN shows timeout..."}]}

        elif ("OUTLOOK_EMAIL" in question_lower):
            result = {"issue_type": "OUTLOOK_EMAIL","chunks": [{"source_file": "email_outlook_troubleshooting_guide.md","chunk_id": "outlook_chunk_012","snippet": ""}]}

        elif ("LAPTOP_PERFORMANCE" in question_lower):
            result = {"issue_type": "LAPTOP_PERFORMANCE","chunks": [{"source_file": "laptop_performance_guide.md","chunk_id": "laptop_chunk_010","snippet": ""}]}

        elif ("PASSWORD_RESET" in question_lower ):
            result = {"issue_type": "PASSWORD_RESET","chunks": [{"source_file": "password_reset_guide.md","chunk_id": "password_chunk_06","snippet": ""}]}

        elif ("NETWORK_CONNECTIVITY" in question_lower):
            result = {"issue_type": "NETWORK_CONNECTIVITY","chunks": [{"source_file": "network_connectivity_guide.md","chunk_id": "network_chunk_07","snippet": ""}]}

        else:
            result = {"issue_type": "OTHER","chunks": [{"source_file": "","chunk_id": "","snippet": ""}]}

    return {"issue_type":result.get("issue_type","OTHER"),"chunks":[{"chunk_id": result.get("chunk_id"),"snippet": result.get("snippet")}]}

def get_user_profile(user_id: str):
    """
   Fetch user information from SQLite.
    """
    query = """SELECT user_id,full_name,department,location,account_status,mfa_status FROM users WHERE user_id = ? """

    result = execute_select_query(query,(user_id,))
    if not result:
        return {"found": False,"message": "Customer not found"}

    cust = result[0]

    return {"found": True,"user": {"user_id": cust["user_id"],
"full_name": cust["full_name"],
"department": cust["department"],
"location": cust["location"],
"account_status": cust["account_status"],
"mfa_status": cust["mfa_status"]}}


def get_device_status(user_id: str):
    """
    Fetch device health and compliance details.
    """
    query = """SELECT user_id,device_id,compliance_status,vpn_client_version,disk_free_percent,cpu_usage_percent,memory_usage_percent FROM devices WHERE user_id = ? """

    result = execute_select_query(query,(user_id,))
    if not result:
        return {"found": False,"message": "Customer not found"}

    cust = result[0]

    return {{
"user_id": cust["user_id"],
"device_id": cust["device_id"],
"compliance_status": cust["compliance_status"],
"vpn_client_version": cust["vpn_client_version"],
"disk_free_percent": cust["disk_free_percent"],
"cpu_usage_percent": cust["cpu_usage_percent"],
"memory_usage_percent": cust["memory_usage_percent"]}}


def check_known_incidents(service_name: str,Status: str):
    """
    Check active incidents by service name, region, or keyword.
    """
    query = """SELECT count,incident_id,service_name,region,severity,status,summary,workaround FROM known_incidents WHERE service_name=?,Status=? """

    result = execute_select_query(query,(service_name,Status))
    if not result:
        return {"found": False,"message": "Incident not found"}

    cust = result[0]

    return {
"count": cust['incident_id'],
"incidents": [{"incident_id": cust['incident_id'],"service_name": cust['service_name'],"region": cust['region'],
"severity": cust['severity'],
"status": cust['status'],
"summary": cust['summary'],
"workaround": cust['workaround']}]}

def run_diagnostic_check(user_id: str):
    """
    Return diagnostic snapshot for a user and device.
    """
    query = """SELECT user_id,vpn_reachable,internet_reachable,webmail_reachable,internal_apps_reachable,account_locked,mfa_push_success FROM diagnostic_snapshots WHERE user_id = ? """

    result = execute_select_query(query,(user_id))
    if not result:
        return {"found": False,"message": "Diagnosis cannot be done"}

    cust = result[0]

    return {
"user_id": cust["user_id"],
"vpn_reachable": cust["vpn_reachable"],
"internet_reachable": cust["internet_reachable"],
"webmail_reachable": cust["webmail_reachable"],
"internal_apps_reachable": cust["internal_apps_reachable"],
"account_locked": cust["account_locked"],
"mfa_push_success": cust["mfa_push_success"]}


def get_ticket_details(user_id: str):
    """
    Fetch existing IT support ticket details.
    """
    query = """SELECT ticket_id,user_id,issue_type,priority,status,subject,assigned_group FROM tickets WHERE user_id = ? """

    result = execute_select_query(query,(user_id))
    if not result:
        return {"found": False,"message": "Ticket not found"}

    cust = result[0]

    return {"ticket_id": cust["ticket_id"],
"user_id": cust["user_id"],
"issue_type": cust["issue_type"],
"priority": cust["priority"],
"status": cust["status"],
"subject": cust["subject"],
"assigned_group": cust["assigned_group"]}


def create_resolution_plan(state):
    """
    This will create resolution plan according to the input
    """
    question = state["user_question"]
    prompt = f"""{SYSTEM_PROMPT}
            Question:{question}"""
    response = llm.invoke(prompt)
    result = safe_json_parse(response.content)

    return {"diagnosis_summary": result["diagnosis_summary"],
"recommended_steps": result["recommended_steps"],
"escalation_required": True,
"escalation_group": result["escalation_group"],
"safety_notes": result["safety_notes"],
"confidence": result["confidence"]}

@tool
def retrieve_troubleshooting_steps(question: str):
    """This is for troubleshooting steps"""
    return retrieve_by_issue(question,"VPN")

@tool
def get_user_profile(question: str):
    """This is for getting user profile details"""
    return retrieve_by_issue(question,"USER_PROFILE")

@tool
def get_device_status(question: str):
    """This is for device status"""
    return retrieve_by_issue(question,"Device_status")

@tool
def check_known_incidents(question: str):
    """THis will check for known incidents"""
    return retrieve_by_issue(question,"incidents")

@tool
def run_diagnostic_check(question: str):
    """THis will diagnose the issue"""
    return retrieve_by_issue(question,"diagnosis")

@tool
def get_ticket_details(question: str):
    """THis will give the ticket details"""
    return retrieve_by_issue(question,"ticket_details")

@tool
def create_resolution_plan(question: str):
    """THis will give resolution plan according to the user query"""
    return retrieve_by_issue(question,"resolution")