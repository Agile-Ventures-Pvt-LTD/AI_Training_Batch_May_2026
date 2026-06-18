from typing import TypedDict, Annotated

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Shared state used across the graph.
    """

    messages: Annotated[list, add_messages]

    tools_used: list

    reflection: str