from typing import Annotated, TypedDict
import ast
from langchain_core.messages import ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from config import llm
from tools import tools
from output_formatter import format_final_response

llm_with_tools = llm.bind_tools(tools, tool_choice="auto")

class AgentState(TypedDict):
    """For agent state."""
    messages: Annotated[list, add_messages]
    user_question: str
    implementation_choice: str
    tools_used: list[str]
    final_response: dict

def agent_node(state: AgentState):
    """For run the LLM."""
    response = llm_with_tools.invoke(state["messages"])
    print("Tool Calls:", response.tool_calls)
    return {"messages": [response]}

def should_continue(state: AgentState):
    """For route the next step."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "finalize"

def reflection_node(state: AgentState):
    """For build the final output."""
    answer = state["messages"][-1].content
    tools_used = []
    for msg in state["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_name = tool_call["name"]
                if tool_name not in tools_used:
                    tools_used.append(tool_name)
    records_found = 0
    for msg in reversed(state["messages"]):
        if not isinstance(msg, ToolMessage):
            continue
        try:
            result = ast.literal_eval(msg.content)
            if isinstance(result, list):
                records_found = len(result)
            elif isinstance(result, dict):
                if result.get("count"):
                    records_found = result["count"]
                elif result.get("results"):
                    records_found = len(result["results"])
                elif result.get("transactions"):
                    records_found = len(result["transactions"])
                elif result.get("flagged_transactions"):
                    records_found = len(result["flagged_transactions"])
        except Exception:
            pass
        break
    final_response = format_final_response(
        state={**state, "tools_used": tools_used},
        answer=answer,
        records_found=records_found,
    )
    return {
        "tools_used": tools_used,
        "final_response": final_response,
    }

def build_graph():
    """Build the graph."""
    flow = StateGraph(AgentState)
    flow.add_node("agent", agent_node)
    flow.add_node("tools", ToolNode(tools))
    flow.add_node("finalize", reflection_node)
    flow.add_edge(START, "agent")
    flow.add_conditional_edges("agent",should_continue,{"tools": "tools", "finalize": "finalize",},)
    flow.add_edge("tools", "finalize")
    flow.add_edge("finalize", END)
    return flow.compile()

compiled_flow = build_graph()