import json
from pydantic import BaseModel, Field
from typing import Literal
from langchain.tools import tool

from db_utils import fetch_one, fetch_all
from retrievers import get_retriever


@tool
def classify_issue_type(user_query: str) -> dict:
    """
    Simple rule-based classifier.

    Using rules because:
    - predictable
    - fast
    - easy to explain
    """

    query = user_query.lower()

    if "vpn" in query:
        issue_type = "VPN"

    elif any(word in query for word in [
        "outlook",
        "email",
        "mailbox",
        "webmail"
    ]):
        issue_type = "OUTLOOK_EMAIL"

    elif any(word in query for word in [
        "slow laptop",
        "slow",
        "cpu",
        "memory",
        "startup"
    ]):
        issue_type = "LAPTOP_PERFORMANCE"

    elif any(word in query for word in [
        "password",
        "login",
        "account locked",
        "mfa"
    ]):
        issue_type = "PASSWORD_RESET"

    elif any(word in query for word in [
        "network",
        "internet",
        "wifi",
        "dns"
    ]):
        issue_type = "NETWORK_CONNECTIVITY"

    elif any(word in query for word in [
        "printer",
        "print"
    ]):
        issue_type = "PRINTER"

    else:
        issue_type = "UNKNOWN"

    return {
        "issue_type": issue_type,
        "confidence": "HIGH",
        "requires_user_lookup": True,
        "requires_device_lookup": True,
        "requires_known_incident_check": True,
        "requires_clarification": issue_type == "UNKNOWN",
        "reasoning_summary": f"Detected {issue_type}"
    }


@tool
def retrieve_troubleshooting_steps(
    issue_type: str,
    query: str
) -> dict:
    """
    Retrieve KB chunks.
    """

    retriever = get_retriever()

    retrieved_docs = retriever.invoke(query)

    chunks = []

    for doc in retrieved_docs:

        document_issue_type = (
            doc.metadata.get("issue_domain")
        )

        if document_issue_type != issue_type:
            continue

        chunks.append(
            {
                "source_file":
                doc.metadata.get("source_file"),

                "chunk_id":
                doc.metadata.get("chunk_id"),

                "snippet":
                doc.page_content[:500]
            }
        )

    return {
        "issue_type": issue_type,
        "chunks": chunks
    }

def find_user_by_partial_name(name):
    
    query = """
    SELECT *
    FROM users
    WHERE lower(full_name)
    LIKE lower(?)
    LIMIT 1
    """

    return fetch_one(
        query,
        (f"%{name}%",)
    )


@tool
def get_user_profile(user_name: str) -> dict:
    
    """
    Lookup user details.
    """
    
    user = find_user_by_partial_name(user_name)

    if not user:
        return {
            "found": False,
            "message": "User not found"
        }

    return {
        "found": True,
        "user": user
    }
    


@tool
def get_device_status(user_id: str) -> dict:
    """
    Device health lookup.
    """

    query = """
    SELECT *
    FROM devices
    WHERE user_id=?
    """

    device = fetch_one(query, (user_id,))

    if not device:
        return {
            "found": False,
            "message": "Device not found"
        }

    return device


@tool
def check_known_incidents(
    keyword: str = ""
) -> dict:
    """
    Check active incidents.
    """

    query = """
    SELECT *
    FROM known_incidents
    WHERE status='Active'
    """

    incidents = fetch_all(query)

    if keyword:

        filtered = []

        for incident in incidents:

            text = json.dumps(incident).lower()

            if keyword.lower() in text:
                filtered.append(incident)

        incidents = filtered

    return {
        "count": len(incidents),
        "incidents": incidents
    }


@tool
def run_diagnostic_check(user_id: str) -> dict:
    """
    Fetch latest diagnostic snapshot.
    """
    query = """
    SELECT *
    FROM diagnostic_snapshots
    WHERE user_id=?
    ORDER BY created_at DESC
    LIMIT 1
    """


    snapshot = fetch_one(query, (user_id,))

    if not snapshot:
        return {
            "found": False,
            "message": "No diagnostics available"
        }

    return snapshot




@tool
def needs_clarification(user_query: str):
    """Detect whether the user's request
    lacks enough information to continue."""
    query = user_query.lower()
    
    
    if "email" in query and len(query.split()) < 4:

        return {
            "clarification_required": True,
            "question":
            (
                "Please provide the user name, "
                "whether Outlook or Webmail is affected, "
                "and any error message."
            )
        }

    return {
        "clarification_required": False
    }


@tool
def get_ticket_details(user_id: str) -> dict:
    """
    Return latest ticket.
    """

    query = """
    SELECT *
    FROM tickets
    WHERE user_id=?
    ORDER BY created_at DESC
    LIMIT 1
    """

    ticket = fetch_one(query, (user_id,))

    if not ticket:
        return {
            "found": False,
            "message": "No ticket found"
        }

    return ticket



ESCALATION_MAP = {
    "VPN": "Network Support",
    "OUTLOOK_EMAIL": "Messaging Support",
    "PASSWORD_RESET": "Identity Access Management",
    "LAPTOP_PERFORMANCE": "Endpoint Support",
    "NETWORK_CONNECTIVITY": "Network Support",
    "PRINTER": "Workplace IT"
}   

class ResolutionPlanSchema(BaseModel):
    diagnosis_summary: str = Field(description="A detailed summary of the diagnosis findings.")
    issue_type: Literal[
        "VPN", 
        "OUTLOOK_EMAIL", 
        "PASSWORD_RESET", 
        "LAPTOP_PERFORMANCE", 
        "NETWORK_CONNECTIVITY", 
        "PRINTER", 
        "UNKNOWN"
    ] = Field(description="The exact issue type as classified earlier. Must be one of the allowed choices.")
    escalation_required: bool = Field(description="Whether the issue requires escalation.")

@tool(args_schema=ResolutionPlanSchema)
def create_resolution_plan(
    diagnosis_summary: str,
    issue_type: str,
    escalation_required: bool
) -> dict:
    """
    Final structured response.
    """

    escalation_group = ESCALATION_MAP.get(
    issue_type,
    ""
    )
    

    if issue_type == "VPN":

        recommended_steps = [
        "Verify internet connectivity",
        "Confirm VPN client version",
        "Check active VPN incidents",
        "Retry using alternate VPN gateway"
        ]

    elif issue_type == "OUTLOOK_EMAIL":
        recommended_steps = [
        "Restart Outlook",
        "Check offline mode",
        "Verify mailbox quota",
        "Create a new Outlook profile if required"
        ]

    elif issue_type == "PASSWORD_RESET":
        recommended_steps = [
        "Check account lock status",
        "Verify reset email delivery",
        "Route to Identity Access Management if issue persists"
        ]

    elif issue_type == "LAPTOP_PERFORMANCE":
        recommended_steps = [
        "Review startup applications",
        "Check disk free space",
        "Restart device",
        "Run endpoint health check"
        ]   

    elif issue_type == "PRINTER":
        recommended_steps = [
        "Follow troubleshooting guide",
        "Collect additional diagnostics"
        ]
    else:
        recommended_steps =[
            "Gather more details from the user",
            "Check general system health",
            "Escalate to general IT support"
        ]

    return {
        "diagnosis_summary": diagnosis_summary,
        "recommended_steps": recommended_steps,
        "escalation_required": escalation_required,
        "escalation_group": escalation_group,
        "safety_notes": [
            "Never ask for password",
            "Never ask for OTP",
            "Never ask for MFA code"
        ],
        "confidence": "HIGH"
    }

@tool
def create_ticket_summary(
    issue_type: str,
    user_name: str,
    summary: str
) -> dict:
    """
    Create support handoff summary.
    """

    return {
        "ticket_summary": summary,
        "issue_type": issue_type,
        "observed_signals": [],
        "diagnostics_checked": [],
        "recommended_assignment_group": "",
        "next_action": "Review and continue troubleshooting"
    }


@tool
def safety_review(text: str):
    """Check generated responses for
    sensitive authentication information."""
    blocked_items = [
        "password",
        "otp",
        "mfa code",
        "private key",
        "security token"
    ]

    violations = []

    for item in blocked_items:

        if item in text.lower():
            violations.append(item)

    return {
        "safe": len(violations) == 0,
        "violations": violations
    }



TOOLS = [
    classify_issue_type,
    retrieve_troubleshooting_steps,
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    get_ticket_details,
    create_resolution_plan,
    create_ticket_summary,
    needs_clarification,
    safety_review
]