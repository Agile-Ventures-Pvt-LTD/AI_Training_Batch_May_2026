import os
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from prompts import system_prompt
from tools import (
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_statement_summary,
    get_rewards_summary,
    get_merchant_spend_summary,
    get_notification_summary,
    detect_suspicious_transactions,
    get_cards_expiring_soon,
    get_top_customers_by_due,
    get_transaction_type_summary,
)

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    plan: str
    reflection: str
    tools_used: list


tools = [
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_statement_summary,
    get_rewards_summary,
    get_merchant_spend_summary,
    get_notification_summary,
    detect_suspicious_transactions,
    get_cards_expiring_soon,
    get_top_customers_by_due,
    get_transaction_type_summary,
]

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

llm_with_tools = llm.bind_tools(tools)


def agent_node(state: AgentState) -> dict:
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm_with_tools.invoke(messages)

    tools_used = list(state.get("tools_used") or [])
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tc in response.tool_calls:
            if tc["name"] not in tools_used:
                tools_used.append(tc["name"])

    return {"messages": [response], "tools_used": tools_used}


def reflection_node(state: AgentState) -> dict:
    last_message = state["messages"][-1]
    content = last_message.content if hasattr(last_message, "content") else ""
    tools_used = state.get("tools_used") or []

    reflection = (
        f"Response generated using {len(tools_used)} tool(s): {', '.join(tools_used)}. "
        f"Answer length: {len(str(content))} characters."
    )

    return {"reflection": reflection}


def route_after_agent(state: AgentState) -> str:
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return "reflection"


graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_node("reflection", reflection_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges(
    "agent",
    route_after_agent,
    {"tools": "tools", "reflection": "reflection"},
)
graph.add_edge("tools", "agent")
graph.add_edge("reflection", END)

custom_agent = graph.compile()
