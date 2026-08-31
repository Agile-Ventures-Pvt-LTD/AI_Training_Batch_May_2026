"""
modern_agent.py

Purpose
-------
Modern LangChain (>=1.0) implementation
for the Ecommerce Database Agent.

Responsibilities
----------------
1. Initialize LLM
2. Register tools
3. Configure system prompt
4. Execute user queries
5. Return business-friendly responses
"""

import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)

from src.prompts.system_prompt import (
    SYSTEM_PROMPT
)


# Load Environment Variables

load_dotenv()


# Initialize LLM

def get_llm():
    """
    Create Groq LLM instance.
    """

    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:

        raise ValueError(
            "GROQ_API_KEY not found in .env file."
        )

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        max_tokens=4000,
        api_key=groq_api_key
    )

    return llm

# Create Agent

def build_agent():
    """
    Build LangChain agent.
    """

    llm = get_llm()

    agent = create_agent(
        model=llm,
        tools=[query_ecommerce_database],
        system_prompt=SYSTEM_PROMPT
    )

    return agent

# Extract Final Text

def get_response_text(response):
    """
    Extract assistant text from
    LangChain response.
    """

    try:

        if isinstance(response, dict):

            messages = response.get(
                "messages",
                []
            )

            if messages:

                return messages[-1].content

        return str(response)

    except Exception:

        return str(response)
    
def run_agent(user_query: str):

    try:

        agent = build_agent()

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_query
                    }
                ]
            }
        )

        return get_response_text(
            response
        )

    except Exception as error:

        return (
            f"Agent Error: {str(error)}"
        )

if __name__ == "__main__":

    query = (
        "Which customers are from Delhi?"
    )

    result = run_agent(query)

    print("\nRESULT\n")
    print(result)