from typing import TypedDict
from typing import Annotated
from langchain_core.messages import SystemMessage
from prompts import SYSTEM_PROMPT

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.graph.message import add_messages

from langgraph.prebuilt import (
    ToolNode,
    tools_condition
)

from langchain_groq import ChatGroq

from tools import tools
from config import GROQ_API_KEY, GROQ_MODEL


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def agent_node(state):

    response = llm_with_tools.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)]
        + state["messages"]
    )

    

    return {
        "messages": [response]
    }

graph = StateGraph(AgentState)

graph.add_node(
    "agent",
    agent_node
)

graph.add_node(
    "tools",
    ToolNode(tools)
)

graph.add_edge(
    START,
    "agent"
)

graph.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END
    }
)

graph.add_edge(
    "tools",
    "agent"
)

compiled_graph = graph.compile()