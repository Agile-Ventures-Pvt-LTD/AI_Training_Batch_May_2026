from typing_extensions import TypedDict, Annotated
from operator import add
from langgraph.graph.message import add_messages

from tools import tools
from graph import custom_agent



class RouterState(TypedDict):
    """
    Represents the state of our query routing workflow.
    """
    customer_query: str                
    query_category: Annotated[list, add]
    retreived_data: str  |None          
    response: str | None                
    error_message: str | None 
    messages: Annotated[list, add_messages]
    reflection: str
    tools_used:  Annotated[list, add]   



def run_custom_agent(query):
    result = custom_agent.invoke(
        {"messages": [("user", query)],"customer_query":query}
    )

    tools_used = []

    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tools_used.extend(
                tool["name"] for tool in msg.tool_calls
            )

    return {
        "query":query,
        "answer": result["messages"][-1].content,
        "tools_used": list(set(tools_used)),
        "reflection": result.get("reflection", "")
    }
