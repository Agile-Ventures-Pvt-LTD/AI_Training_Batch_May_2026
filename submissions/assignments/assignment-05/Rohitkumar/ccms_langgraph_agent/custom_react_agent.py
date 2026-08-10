from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from config import GROQ_API_KEY, GROQ_MODEL
from prompts import SYSTEM_PROMPT
from tools import *


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"


def agent_node(state: AgentState):
    """Agent node that decides which tool to call and generates final answer."""
    messages = state["messages"]
    llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)

    tools = [
        inspect_database_schema,
        get_customer_profile,
        get_card_details,
        search_transactions,
        get_customer_transactions,
        get_rewards_summary,
        get_merchant_spend_summary,
        detect_suspicious_transactions,
        get_statement_summary,
        get_notification_summary,
        get_cards_expiring_soon,
        get_top_customers_by_due,
        get_transaction_type_summary
    ]

    llm_with_tools = llm.bind_tools(tools)

    response = llm_with_tools.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        *messages
    ])

    return {"messages": [response]}


def build_custom_react_agent():
    """Build and compile the custom LangGraph ReAct agent."""
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode([
        inspect_database_schema,
        get_customer_profile,
        get_card_details,
        search_transactions,
        get_customer_transactions,
        get_rewards_summary,
        get_merchant_spend_summary,
        detect_suspicious_transactions,
        get_statement_summary,
        get_notification_summary,
        get_cards_expiring_soon,
        get_top_customers_by_due,
        get_transaction_type_summary
    ]))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, {
        "tools": "tools",
        "end": END
    })
    workflow.add_edge("tools", "agent")

    return workflow.compile()


custom_agent = build_custom_react_agent()