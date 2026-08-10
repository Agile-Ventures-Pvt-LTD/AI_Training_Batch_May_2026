
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, SystemMessage

from config import GROQ_API_KEY, GROQ_MODEL
from langchain_groq import ChatGroq
from tools import get_customer_profile, get_inspect_schema, get_card_details, search_transactions,get_customer_transactions,get_merchant_spend_summary,detect_suspicious_transactions
from prompts import SYSTEM_PROMPT


llm = ChatGroq(model=GROQ_MODEL, groq_api_key=GROQ_API_KEY, temperature=0)

tools = [
    get_customer_profile,
    get_inspect_schema,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_merchant_spend_summary,
    detect_suspicious_transactions
]
llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def agent_node(state: AgentState):
    """This node passes the conversation to Groq to get a response or a tool call."""
    messages = state["messages"]
    
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def reflection_node(state: AgentState):
    """This node ensures the final output is clean and masked."""
    messages = state["messages"]
    last_message = messages[-1]
    
    reflection_prompt = f"""
    Review this final answer: {last_message.content}
    Ensure no full credit card numbers or security codes are visible. 
    Make it sound polite and business-friendly. Return only the revised text.
    """
    reflection_response = llm.invoke([HumanMessage(content=reflection_prompt)])
    return {"messages": [reflection_response]}

graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_node("reflection", reflection_node)

graph.add_edge(START, "agent")

graph.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: "reflection"})

graph.add_edge("tools", "agent")
graph.add_edge("reflection", END)


custom_agent = graph.compile()