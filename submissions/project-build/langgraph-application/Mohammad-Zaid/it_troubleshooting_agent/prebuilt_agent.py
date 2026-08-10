from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
import json
import os
from datetime import datetime
from config import GROQ_API_KEY, GROQ_MODEL
from tools import (
    retrieve_troubleshooting_steps,
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    get_ticket_details,
    create_resolution_plan,
)


llm = ChatGroq(model=GROQ_MODEL, temperature=0.0, api_key=GROQ_API_KEY)


@tool
def kb_search(query: str) -> str:
    """Search knowledge base for troubleshooting steps"""
    return str(retrieve_troubleshooting_steps(query))


@tool
def user_info(user_id: str) -> str:
    """Get user profile"""
    return str(get_user_profile(user_id))


@tool
def device_info(user_id: str) -> str:
    """Get device status"""
    return str(get_device_status(user_id))


@tool
def incidents() -> str:
    """Check known incidents"""
    return str(check_known_incidents())


@tool
def diagnostics(user_id: str) -> str:
    """Run diagnostic check"""
    return str(run_diagnostic_check(user_id))


@tool
def tickets(user_id: str) -> str:
    """Get ticket details"""
    return str(get_ticket_details(user_id))


@tool
def resolution(user_id: str, issue: str) -> str:
    """Create resolution plan"""
    return str(create_resolution_plan(user_id, issue))


tools = [kb_search, user_info, device_info, incidents, diagnostics, tickets, resolution]
agent = create_react_agent(llm, tools)


def format_output(response, user_query):
    """Format response into required JSON structure"""
    output = {
        "timestamp": datetime.now().isoformat(),
        "user_query": user_query,
        "issue_type": "System",
        "diagnosis_summary": "",
        "evidence_used": {"kb_sources": [], "tools_used": [], "diagnostic_signals": []},
        "recommended_steps": [],
        "escalation_required": False,
        "escalation_group": "",
        "safety_notes": [],
        "confidence": "MEDIUM"
    }
    
    if not isinstance(response, dict) or "messages" not in response:
        return output
    
    messages = response["messages"]
    if not messages:
        return output
    
    # Extract diagnosis
    last_msg = messages[-1]
    if hasattr(last_msg, 'content'):
        content = last_msg.content
        output["diagnosis_summary"] = content[:1000]
        
        # Extract steps
        for line in content.split("\n"):
            if any(x in line.lower() for x in ["step", "check", "verify", "try"]):
                output["recommended_steps"].append(line.strip())
    
    # Extract tools used
    for msg in messages:
        if hasattr(msg, 'tool_calls'):
            for call in msg.tool_calls:
                if hasattr(call, 'name'):
                    output["evidence_used"]["tools_used"].append(call.name)
    
    # Determine issue type
    query_lower = user_query.lower()
    if "vpn" in query_lower or "network" in query_lower:
        output["issue_type"] = "Network/Connectivity"
    elif "memory" in query_lower or "slow" in query_lower:
        output["issue_type"] = "Performance"
    elif "password" in query_lower or "access" in query_lower:
        output["issue_type"] = "Access/Authentication"
    elif "email" in query_lower or "outlook" in query_lower:
        output["issue_type"] = "Messaging"
    
    # Escalation check
    diag_lower = output["diagnosis_summary"].lower()
    if "escalat" in diag_lower or "critical" in diag_lower:
        output["escalation_required"] = True
        if "network" in diag_lower:
            output["escalation_group"] = "Network Support"
        elif "email" in diag_lower:
            output["escalation_group"] = "Messaging Support"
        else:
            output["escalation_group"] = "IT Support"
    
    # Confidence
    evidence_count = len(output["evidence_used"]["tools_used"])
    output["confidence"] = "HIGH" if evidence_count >= 4 else ("MEDIUM" if evidence_count >= 2 else "LOW")
    
    # Safety notes
    if "password" in user_query.lower():
        output["safety_notes"].append("Do not ask for passwords")
    if "mfa" in user_query.lower():
        output["safety_notes"].append("Do not ask for MFA codes")
    
    return output


def save_results(result: dict, filename: str = "outputs/evaluation_results.json"):
    """Save results to JSON file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    existing_results = []
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                existing_results = data if isinstance(data, list) else [data]
        except:
            pass
    
    existing_results.append(result)
    
    with open(filename, "w") as f:
        json.dump(existing_results, f, indent=2)


def solve(query: str, save_output: bool = True):
    """Solve IT troubleshooting issue"""
    response = agent.invoke({"messages": [("user", query)]})
    output = format_output(response, query)
    
    if save_output:
        save_results(output)
    
    return output
