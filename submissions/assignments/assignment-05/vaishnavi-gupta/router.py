from langchain_core.messages import AIMessage


def route_after_agent(state):

    last_message = state["messages"][-1]

    if (
        isinstance(last_message, AIMessage)
        and last_message.tool_calls
    ):
        return "tools"

    return "reflection"