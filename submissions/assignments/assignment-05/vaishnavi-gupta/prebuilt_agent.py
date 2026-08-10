import json
from langchain_groq import ChatGroq
from prompts import SYSTEM_PROMPT
from tools import TOOLS
from langgraph.prebuilt import create_react_agent
from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

def get_llm():

    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0
    )


def build_agent():
    """
    Build LangGraph Prebuilt ReAct Agent.
    """

    llm = get_llm()

    agent = create_react_agent(
        model=llm,
        tools=TOOLS,
        prompt=SYSTEM_PROMPT
    )

    return agent


agent = build_agent()


def ask_agent(question: str):

    response = agent.invoke(
        {
            "messages": [
                ("user", question)
            ]
        }
    )

    messages = response["messages"]

    tool_used = "Not Available"
    records_found = "Unknown"
    masked = True

    for msg in messages:

        if msg.__class__.__name__ == "ToolMessage":

            tool_used = getattr(
                msg,
                "name",
                "Not Available"
            )

            try:

                data = json.loads(
                    msg.content
                )

                records_found = data.get(
                    "records_found",
                    "Unknown"
                )

                masked = data.get(
                    "sensitive_data_masked",
                    True
                )

            except Exception:
                pass

    answer = messages[-1].content

    return {
        "tool_used": tool_used,
        "records_found": records_found,
        "answer": answer,
        "sensitive_data_masked": masked
    }