from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from tools import (
    retrieve_troubleshooting_steps,
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    get_ticket_details,
    create_resolution_plan,
)
from config import GROQ_API_KEY, GROQ_MODEL


llm = ChatGroq(model=GROQ_MODEL, temperature=0.0, api_key=GROQ_API_KEY)


@tool
def retrieve_troubleshooting_steps_tool(query: str) -> str:
    """Search knowledge base for troubleshooting steps"""
    return str(retrieve_troubleshooting_steps(query))


@tool
def get_user_profile_tool(user_id: str) -> str:
    """Get user profile information"""
    return str(get_user_profile(user_id))


@tool
def get_device_status_tool(user_id: str) -> str:
    """Get device status and compliance information"""
    return str(get_device_status(user_id))


@tool
def check_known_incidents_tool() -> str:
    """Check for active known incidents"""
    return str(check_known_incidents())


@tool
def run_diagnostic_check_tool(user_id: str) -> str:
    """Run diagnostic check on user's device"""
    return str(run_diagnostic_check(user_id))


@tool
def get_ticket_details_tool(user_id: str) -> str:
    """Get user's ticket details"""
    return str(get_ticket_details(user_id))


@tool
def create_resolution_plan_tool(user_id: str, issue: str) -> str:
    """Create resolution plan for user issue"""
    return str(create_resolution_plan(user_id, issue))


tools = [
    retrieve_troubleshooting_steps_tool,
    get_user_profile_tool,
    get_device_status_tool,
    check_known_incidents_tool,
    run_diagnostic_check_tool,
    get_ticket_details_tool,
    create_resolution_plan_tool,
]

agent_executor = create_react_agent(llm, tools)


def run_agent(user_query: str):
    """Run the IT troubleshooting agent"""
    result = agent_executor.invoke({"messages": [("user", user_query)]})
    return result


if __name__ == "__main__":
    question = str(input("Enter your Question"))
    print(f"User: {question}\n")
    response = run_agent(question)
    print(f"Agent Response:\n{response}")
