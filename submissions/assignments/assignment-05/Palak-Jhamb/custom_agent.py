from tools import tools
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from config import get_api_key
from operator import add




class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    plan: str
    reflection: str
    tools_used:  Annotated[list, add]

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=get_api_key(),
)
llm_with_tools = llm.bind_tools(tools, tool_choice="auto")

tool_node = ToolNode(tools)

def call_model(state: AgentState) -> dict:
    """Invokes the LLM with the current message history."""
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    tool_names = [tool["name"] for tool in response.tool_calls]

    return {"messages": [response],"tools_used": tool_names}


from langchain_core.messages import HumanMessage
def reflection_node(state: AgentState) -> dict:
    """
    Reflect on the agent's reasoning and tool usage.
    """
    tools_used = state.get("tools_used", [])
    mesages=state.get("messages")
    prompt = f"""
    Review the completed task.
    Act as an testing agent and your task is to reflect on completed task.
    Tools used:
    {tools_used}
    Mesages:
    {mesages}
    Evaluate:
    1. Were the correct tools selected?
    2. Was any tool unnecessary?
    3. Is the final answer complete?
   

    Give a concise reflection.
    """

    reflection = llm.invoke([HumanMessage(content=prompt)]).content
    return {"reflection": reflection}


graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools_node", tool_node)
graph.add_node("reflection_node", reflection_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition,
    {
        "tools": "tools_node",
        "__end__": "reflection_node" 
    })
graph.add_edge("tools_node", "agent")
graph.add_edge("reflection_node", END)

custom_agent = graph.compile()

def run_custom_agent(query):
    result = custom_agent.invoke(
        {"messages": [("user", query)]}
    )

    tools_used = []

    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tools_used.extend(
                tool["name"] for tool in msg.tool_calls
            )

    return {
        "answer": result["messages"][-1].content,
        "tools_used": list(set(tools_used)),
        "reflection": result.get("reflection", "")
    }
