from config import llm
from tools import custom_tools
from langgraph.prebuilt import ToolNode
from typing import Annotated, TypedDict, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph

# State Class
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Condition Check to end the graph or continue
def should_continue(state: State) -> Literal["action", END]: # type: ignore
    """Determines whether to continue the loop or end."""

    last_message = state['messages'][-1]

    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "action"
    
    else:
        return END

# Custom ReAct Agent
def call_model(state: State) -> dict:
    """Invokes the LLM with the current message history."""

    messages = state['messages']

    try:
        response = llm_with_tools.invoke(messages)
    except Exception as e:
        print(e)
    
    return {"messages": [response]}


tool_node = ToolNode(custom_tools)
llm_with_tools = llm.bind_tools(custom_tools, tool_choice="auto")


# Making the Workflow of the graph
workflow = StateGraph(State)

# Graph nodes
workflow.add_node("reason", call_model)
workflow.add_node("action", tool_node)

# Graph Edges
workflow.add_edge(START, "reason")

# Conditional Edge
workflow.add_conditional_edges(
    "reason",
    should_continue
)

workflow.add_edge("action", "reason")

# Final agent to get the answers
agent_workflow = workflow.compile()