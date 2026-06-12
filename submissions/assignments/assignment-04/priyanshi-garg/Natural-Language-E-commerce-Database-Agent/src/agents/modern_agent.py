from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain_groq import ChatGroq

from src.prompts.system_prompt import (
    SYSTEM_PROMPT
)

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)


def create_modern_agent():

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    agent = create_agent(
        model=llm,
        tools=[
            query_ecommerce_database
        ],
        system_prompt=SYSTEM_PROMPT
    )

    return agent