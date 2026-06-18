from tools import (inspect_schema,customer_profile,card_details,transactions_search,customer_transactions,suspicious_transactions,
                   rewards_summary,merchant_spend_summary)

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from config import MODEL_NAME, GROQ_API_KEY
from prompts import system_prompt
from typing import Annotated, TypedDict , Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

system_prompt=system_prompt()


tools = [inspect_schema,customer_profile,card_details,transactions_search,customer_transactions,suspicious_transactions,
        rewards_summary,merchant_spend_summary]

llm = ChatGroq(model=MODEL_NAME,groq_api_key=GROQ_API_KEY)

llm_with_tools = llm.bind_tools(tools, tool_choice="auto")

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    # plan: str
    # reflection: str
    # tools_used: list
    # tool_count: int

def agent_node(state: AgentState) -> dict:

    """Invokes the LLM with the current message history."""
    print("---LLM NODE---")

    messages = state['messages']

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}

def reflection_node(state: AgentState):
    """
    Improve the final response before showing it to the user.
    """
    answer = state["messages"][-1].content
    prompt = f"""
    Improve the response slightly.
    Keep all database details unchanged.
    Remove only sensitive information (card numbers, CVV, PIN, passwords).
    Do not add new content
    Response:
    {answer}
    """
    final_response = llm.invoke(prompt)
    return {
        "messages": [final_response]
    }


def route_agent(state: AgentState):
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return "reflection"

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_node("reflection", reflection_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges(
    "agent",
    route_agent,
    {
        "tools": "tools",
        "reflection": "reflection"
    }
)
graph.add_edge("tools", "agent")
graph.add_edge("reflection", END)
compiled_graph = graph.compile()

def custom_agent(user_input):
    try: 
        message_input = [SystemMessage(content=system_prompt), HumanMessage(content=user_input)]
        response = compiled_graph.invoke({"messages": message_input})
        return response["messages"][-1].content
    except Exception as e:
        return f"Error: {e}"