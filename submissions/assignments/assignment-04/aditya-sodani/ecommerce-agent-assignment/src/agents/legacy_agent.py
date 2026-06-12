import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain.agents import (
    initialize_agent,
    AgentType,
)

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database,
)

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

tools = [
    query_ecommerce_database,
]

agent = initialize_agent(
    tools=tools,
    llm=llm,

    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,

    verbose=True,

    handle_parsing_errors=True,

    max_iterations=5,

    early_stopping_method="generate",
)