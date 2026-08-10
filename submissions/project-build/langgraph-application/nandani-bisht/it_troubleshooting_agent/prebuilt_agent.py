from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from config import GROQ_API_KEY, GROQ_MODEL
from prompts import SYSTEM_PROMPT
from tools import (
    inspect_database_schema,
    classify_issue_type,
    retrieve_troubleshooting_steps,
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    get_ticket_details,
    search_tickets,
    get_active_incidents,
)

llm = ChatGroq(
    model=GROQ_MODEL,
    groq_api_key=GROQ_API_KEY,
)

tools = [
    inspect_database_schema,
    classify_issue_type,
    retrieve_troubleshooting_steps,
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    get_ticket_details,
    search_tickets,
    get_active_incidents,
]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT,
)


def run_prebuilt_agent(query: str, verbose: bool = True):
    if verbose:
        print("\n" + "=" * 60)
        print("IT TROUBLESHOOTING AGENT (Pre-built ReAct)")
        print("=" * 60)
        print(f"Query: {query}")
        print("-" * 60)

    result = agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"recursion_limit": 50},
    )

    response = result["messages"][-1].content

    if verbose:
        print("\nAgent Response:")
        print(response)
        print("=" * 60)

    return response