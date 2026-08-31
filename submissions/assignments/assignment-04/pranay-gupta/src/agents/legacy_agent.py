# src/agents/legacy_agent.py

import os

from dotenv import load_dotenv

from langchain.agents import (
    initialize_agent,
    AgentType
)

from langchain_groq import ChatGroq

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)

from src.prompts.system_prompt import (
    SYSTEM_PROMPT
)

load_dotenv()


def create_legacy_agent():
    """
    Legacy LangChain Agent
    Compatible with langchain < 1.0
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    tools = [
        query_ecommerce_database
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        agent_kwargs={
            "prefix": SYSTEM_PROMPT
        }
    )

    return agent


legacy_agent = create_legacy_agent()


def run_legacy_agent(user_query: str) -> str:
    """
    Execute a business query using
    the legacy LangChain agent.
    """

    try:
        response = legacy_agent.run(user_query)

        return response

    except Exception as error:
        return (
            f"Legacy Agent Error: {str(error)}"
        )
