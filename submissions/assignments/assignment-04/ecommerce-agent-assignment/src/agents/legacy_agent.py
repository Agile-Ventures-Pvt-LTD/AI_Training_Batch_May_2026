"""
legacy_agent.py

Purpose
-------
Legacy LangChain implementation
using initialize_agent().

This demonstrates the older
LangChain agent architecture
required by the assignment.

Responsibilities
----------------
1. Initialize LLM
2. Register tools
3. Create ReAct Agent
4. Execute queries
"""

import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain.agents import (
    initialize_agent,
    AgentType
)

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)

# Load Environment Variables

load_dotenv()


# Initialize LLM

def get_llm():
    """
    Create Groq LLM.
    """

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GROQ_API_KEY not found."
        )

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        max_tokens=4000,
        api_key=api_key
    )

    return llm


# Build Legacy Agent

def build_legacy_agent():
    """
    Create legacy LangChain agent.
    """

    llm = get_llm()

    tools = [
        query_ecommerce_database
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent

# Run Agent

def run_legacy_agent(
    user_query: str
):
    """
    Execute user query.
    """

    try:

        agent = build_legacy_agent()

        response = agent.run(
            user_query
        )

        return response

    except Exception as error:

        return (
            f"Legacy Agent Error: "
            f"{str(error)}"
        )
    
# Local Testing

if __name__ == "__main__":

    query = (
        "What is total revenue?"
    )

    result = run_legacy_agent(
        query
    )

    print("\nRESULT\n")
    print(result)