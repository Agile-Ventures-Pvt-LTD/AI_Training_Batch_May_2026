from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
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


def solve(query: str):
    return agent.invoke({"messages": [("user", query)]})
