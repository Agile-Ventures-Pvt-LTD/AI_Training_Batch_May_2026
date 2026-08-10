# choice 1
from langchain_groq import ChatGroq

from langchain.agents import create_agent

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

from prompts import SYSTEM_PROMPT

from tools import TOOLS


def build_agent():

    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0
    )

    agent = create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT
    )

    return agent


def run_agent(query: str):

    agent = build_agent()
    response = agent.invoke(
        {"messages": [("user", query)]}
        )

    return response