from config import llm
from typing import Optional
from langchain.tools import tool
from retrievers import retriever
from db_utils import execute_query
from prompts import resoultion_prompt
from langchain.tools.retriever import create_retriever_tool

retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="retrieve_troubleshooting_steps",
    description="Search and return information about the troubleshooting steps from Knowledge_base."
)


@tool
def get_user_profile(
    user_id: str,
    full_name: Optional[str] = None,
    email: Optional[str] = None
):
    """
    Retrieve a user profile from the database.
    """
    query = """
    SELECT user_id, full_name, department, location, account_status, mfa_status
    FROM users
    WHERE user_id = ?
    """
    params = [user_id]

    if full_name:
        query += " AND full_name = ?"
        params.append(full_name)

    if email:
        query += " AND email = ?"
        params.append(email)

    result = execute_query(query, tuple(params))

    return f"{result}"


@tool
def get_device_status(user_id: str, device_id: Optional[str]):
    """
    Give the Device Status using the user_id and device_id
    """

    query = """SELECT user_id, device_id, compliance_status, vpn_client_version, disk_free_percent, cpu_usage_percent, memory_usage_percent
    FROM devices
    """

    params = []

    if user_id and device_id:
        query += " WHERE user_id = ? AND device_id = ?"
        params.append(user_id)
        params.append(device_id)

    else:
        if user_id or device_id:
            query += " WHERE"

        if user_id:
            query += " user_id = ?"
            params.append(user_id)

        if device_id:
            query += " device_id = ?"
            params.append(device_id)

    result = execute_query(query, tuple(params))

    return f"{result}"



@tool
def check_known_incidents(
    service_name: Optional[str] = None,
    region: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Check active incidents by service name, region, or status.
    """
    query = """
    SELECT incident_id, service_name, region, severity, status, summary, workaround
    FROM known_incidents
    WHERE 1 = 1
    AND (service_name = ? OR ? IS NULL)
    AND (region = ? OR ? IS NULL)
    AND (status = ? OR ? IS NULL)
    """
    params = (service_name, service_name, region, region, status, status)
    result = execute_query(query, params)

    return {
        "count": len(result),
        "incidents": result
    }


@tool
def run_diagnostic_check(user_id: str, device_id: Optional[str]):
    """
    Return diagnostic snapshot for a user_id and device_id.
    """
    
    query = """
    SELECT user_id, vpn_reachable, internet_reachable, webmail_reachable, internal_apps_reachable, account_locked, mfa_push_success
    FROM diagnostic_snapshots
    WHERE user_id = ? AND (device_id = ? OR IS NULL)
    """
    
    result = execute_query(query, (user_id, device_id))
    
    return f"{result}"


@tool
def get_ticket_details(ticket_id: str):
    """
    Fetch the existing IT support ticket details.
    """
    query = """
    SELECT ticket_id, user_id, issue_type, priority, status, subject, assigned_group
    FROM tickets
    WHERE ticket_id = ?;
    """

    result = execute_query(query, (ticket_id,))

    return f"{result}" 


@tool
def generate_resolution_plan(context):
    """
    Generate the resolution plan based on 
    - User issue
    - Trouble shooting
    - Known incidents
    - Diagnostic Run
    """

    return llm.invoke(resoultion_prompt.format(**context)).content


@tool
def get_active_incidents(service_name: Optional[str] = None, region: Optional[str] = None,):
    """
    Give the active incidents on the basic service_name or region or overall
    """

    query = """
    SELECT * FROM known_incidents
    WHERE status = 'Active'
    AND (region = ? OR ? IS NULL)
    AND (service_name = ? OR ? IS NULL);
    """

    params = (service_name, service_name, region, region)
    result = execute_query(query, params)

    return f"{result}"


@tool
def create_ticket_summary(ticket_id: str):
    """
    Generate the ticket summary on the basic of the ticket_id
    """

    query = "SELECT * FROM tickets WHERE ticket_id = ?;"

    ticket = execute_query(query, (ticket_id,))

    prompt = {
        "role" : "system",
        "content" : f"""
        Role:
        You are an Expert at summarizing the ticket details

        Your tass is to summarize this ticket:
        Ticket: {ticket}
        """
    }   

    result = llm.invoke(prompt)

    return result


@tool
def classify_issue_type():
    """
    Generate the type of the issue depending upon the user query
    """

    prompt = {
        "role" : "system",
        "content" : """
        Your task is to classify the user query into any of this types:

        VPN
        OUTLOOK_EMAIL
        LAPTOP_PERFORMANCE
        PASSWORD_RESET
        NETWORK_CONNECTIVITY
        PRINTER
        UNKNOWN
        """
    }

    result = llm.invoke(prompt)

    return result.content


tools = [
    retriever_tool, 
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    get_ticket_details,
    generate_resolution_plan,
    get_active_incidents,
    create_ticket_summary,
    classify_issue_type
]