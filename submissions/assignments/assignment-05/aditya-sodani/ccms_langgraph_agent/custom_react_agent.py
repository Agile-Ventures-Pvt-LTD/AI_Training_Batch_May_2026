from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from tools import tools
from prompts import SYSTEM_PROMPT
from config import config
llm = ChatGroq(
    model=config.GROQ_MODEL,
    temperature=0,
    api_key=config.GROQ_API_KEY
)
llm_with_tools = llm.bind_tools(tools)
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
def agent_node(state: AgentState):
    response = llm_with_tools.invoke(
        [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        + state["messages"]
    )
 
    return {
        "messages": [response]
    }
def reflection_node(state: AgentState):
    return state
tool_node = ToolNode(tools)
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_node("reflection", reflection_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent",tools_condition,{"tools": "tools","__end__": "reflection"})
graph.add_edge("tools", "agent")
graph.add_edge("reflection", END)
custom_agent_executor = graph.compile()
 