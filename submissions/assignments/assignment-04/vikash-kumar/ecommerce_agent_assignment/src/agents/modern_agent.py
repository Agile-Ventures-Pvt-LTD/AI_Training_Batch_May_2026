from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from src.tools.ecommerce_sql_tool import query_ecommerce_database

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

tools = [query_ecommerce_database]

agent = create_react_agent(
    model=llm,
    tools=tools
)