from langgraph.graph import (
    StateGraph,
    START,
    END
)

from state import AgentState

from nodes import (
    agent_node,
    tool_node,
    reflection_node
)

from router import route_after_agent


def build_agent():

    workflow = StateGraph(
        AgentState
    )

    workflow.add_node(
        "agent",
        agent_node
    )

    workflow.add_node(
        "tools",
        tool_node
    )

    workflow.add_node(
        "reflection",
        reflection_node
    )

    workflow.add_edge(
        START,
        "agent"
    )

    workflow.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            "reflection": "reflection"
        }
    )

    workflow.add_edge(
        "tools",
        "agent"
    )

    workflow.add_edge(
        "reflection",
        END
    )

    return workflow.compile()


graph = build_agent()


def ask_agent(question: str):

    result = graph.invoke(
        {
            "messages": [
                (
                    "user",
                    question
                )
            ],
            "tools_used": [],
            "reflection": ""
        }
    )

    messages = result["messages"]

    final_answer = ""

    for msg in reversed(messages):

        if hasattr(msg, "content"):

            content = str(msg.content).strip()

            if content:
                final_answer = content
                break

    tool_used = "Not Available"

    if result.get("tools_used"):

        tool_used = ", ".join(
            result["tools_used"]
        )

    return {
        "tool_used": tool_used,
        "records_found": "N/A",
        "answer": final_answer,
        "sensitive_data_masked": True,
        "reflection": result.get(
            "reflection",
            ""
        )
    }