from dotenv import load_dotenv

load_dotenv()

from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_groq import ChatGroq

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)


def create_legacy_agent():

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )

    agent = initialize_agent(
        tools=[query_ecommerce_database],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent