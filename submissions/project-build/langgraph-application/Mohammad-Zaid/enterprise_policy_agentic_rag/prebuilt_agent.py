# file: prebuilt_agent.py

from langgraph.prebuilt import create_react_agent

from langchain_groq import ChatGroq

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

from prompts import SYSTEM_PROMPT

from tools import (
    retrieve_hr_policy,
    retrieve_travel_policy,
    retrieve_reimbursement_policy,
    retrieve_it_security_policy,
    retrieve_ai_usage_policy,
    grade_context
)


def get_agent():

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found"
        )

    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0
    )

    tools = [
        retrieve_hr_policy,
        retrieve_travel_policy,
        retrieve_reimbursement_policy,
        retrieve_it_security_policy,
        retrieve_ai_usage_policy,
        grade_context
    ]

    agent = create_react_agent(
        llm,
        tools
    )

    return agent


def ask_agent(question):

    agent = get_agent()

    response = agent.invoke(
        {
            "messages": [
                (
                    "system",
                    SYSTEM_PROMPT
                ),
                (
                    "user",
                    question
                )
            ]
        }
    )

    return response["messages"][-1].content