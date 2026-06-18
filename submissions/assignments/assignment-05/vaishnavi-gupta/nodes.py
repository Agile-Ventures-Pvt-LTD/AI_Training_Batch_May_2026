from langchain_groq import ChatGroq
from prompts import SYSTEM_PROMPT
from tools import TOOLS
from langgraph.prebuilt import ToolNode

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0
)


llm_with_tools = llm.bind_tools(TOOLS)


def agent_node(state):

    response = llm_with_tools.invoke(
        [
            (
                "system",
                SYSTEM_PROMPT
            )
        ]
        + state["messages"]
    )

    return {
        "messages": [response]
    }


tool_node = ToolNode(TOOLS)


def reflection_node(state):

    messages = state["messages"]

    tools_used = []

    for msg in messages:

        if hasattr(msg, "name") and msg.name:
            tools_used.append(msg.name)

    return {
        "reflection": (
            "Response generated successfully."
        ),
        "tools_used": list(set(tools_used))
    }