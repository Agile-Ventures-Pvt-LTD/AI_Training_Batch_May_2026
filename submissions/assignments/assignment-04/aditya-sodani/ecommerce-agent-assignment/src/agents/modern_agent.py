import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from src.tools.ecommerce_sql_tool import query_ecommerce_database
from src.prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

agent = create_agent(
    model=llm,
    tools=[query_ecommerce_database],
    system_prompt=SYSTEM_PROMPT
)