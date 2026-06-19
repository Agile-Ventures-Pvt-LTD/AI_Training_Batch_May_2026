import json
from langchain_core.tools import tool
import db_utils
import retrievers
import config
import prompts
from langchain_groq import ChatGroq

@tool
def retrieve_steps(issue_type,query,):
    """ retrieve relevant chunks from the knowledge base"""
    retriever=retrievers.get_retriever()
    results=retriever.similarity_search(query,k=3,filter_domain=issue_type)
    chunks=[]
    for res in results:
        chunks.append({
            "source_file": res["metadata"].get("source_file"),
            "chunk_id": res["metadata"].get("chunk_id"),
            "snippet": res["content"]})
    output={
        "issue_type": issue_type,
        "chunks": chunks}
    return json.dumps(output, indent=2)

@tool
def get_user_profile(user_id=None,full_name=None,email=None):
    """ get user profile and details from sqlite by id, name or email"""
    profile=db_utils.user_profile(user_id=user_id,full_name=full_name,email=email)
    if not profile:
        return json.dumps({"found": False, "message": "profile not found"})
    return json.dumps({
        "found": True,
        "user": profile
    }, indent=2)

@tool
def get_device_status(user_id=None, device_id=None):
    """get device specs and details of device"""
    device=db_utils.device_status(user_id=user_id,device_id=device_id)
    if not device:
        return json.dumps({"found": False, "message": "device not found"})
    return json.dumps(device, indent=2)

@tool
def check_known_incidents(service_name=None, region=None, status="Active"):
    """query database for active service outages or incidents filtered by service name and region."""
    incidents=db_utils.known_incidents(service_name=service_name,region=region,status=status)
    return json.dumps({
        "count": len(incidents),
        "incidents": incidents
    }, indent=2)

@tool
def run_diagnostic_check(user_id=None, device_id=None):
    """run diagnostic network tests and mfa check"""
    snapshot=db_utils.diagnostic_snapshot(user_id=user_id,device_id=device_id)
    if not snapshot:
        return json.dumps({"found": False, "message": "no snapshot found"})
    return json.dumps(snapshot, indent=2)

@tool
def get_ticket_details(ticket_id=None, user_id=None):
    """ get details of specific ticket """
    ticket=db_utils.ticket_details(ticket_id=ticket_id,user_id=user_id)
    if not ticket:
        return json.dumps({"found": False, "message": "ticket details were not found"})
    return json.dumps(ticket, indent=2)

@tool
def create_plan(diagnosis_summary,recommended_steps,escalation_required, escalation_group= None, safety_notes = None, confidence = "HIGH"):
    """ create a final resolution or escalation plan """
    plan = {
        "diagnosis_summary": diagnosis_summary,
        "recommended_steps": recommended_steps,
        "escalation_required": escalation_required,
        "escalation_group": escalation_group or "",
        "safety_notes": safety_notes or [],
        "confidence": confidence}
    return json.dumps(plan, indent=2)

@tool
def classify_issue_type(query):
    """ classify the issue type of the user query """
    llm = ChatGroq(
        groq_api_key=config.GROQ_API_KEY,
        model_name=config.GROQ_MODEL,
        temperature=0
    )
    response = llm.invoke(prompts.CLASSIFICATION_PROMPT.format(user_query=query))
    return response.content.strip()

@tool
def create_ticket_summary(user_id: str = None, issue_type: str = None, summary_details: str = None):
    """ create a ticket summary to log the incident """
    ticket = {
        "user_id": user_id or "unknown",
        "issue_type": issue_type or "unknown",
        "summary": summary_details or "unknown",
        "status": "Logged"
    }
    return json.dumps(ticket, indent=2)

@tool
def check_escalation_required(diagnosis_summary, severity):
    """ check if the issue requires escalation based on severity or metrics """
    required = severity.upper() == "HIGH" or "latency" in diagnosis_summary.lower() or "timeout" in diagnosis_summary.lower()
    return json.dumps({
        "escalation_required": required,
        "reason": "High severity or critical service impact detected" if required else "Standard issue, handle via first-level checks"
    }, indent=2)

@tool
def search_tickets(query_term):
    """ search existing tickets in the system by query_term in subject or description """
    tickets = db_utils.search_tickets(query_term)
    return json.dumps({
        "count": len(tickets),
        "tickets": tickets
    }, indent=2)

@tool
def get_active_incidents(service_name= None, region = None):
    """ get active outages or incidents filtered by service name and region """
    incidents = db_utils.known_incidents(service_name=service_name, region=region, status="Active")
    return json.dumps({
        "count": len(incidents),
        "incidents": incidents
    }, indent=2)

TOOLS=[
    retrieve_steps,
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    get_ticket_details,
    create_plan,
    classify_issue_type,
    create_ticket_summary,
    check_escalation_required,
    search_tickets,
    get_active_incidents
]