from dotenv import load_dotenv

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase

from langchain_groq import ChatGroq

from src.tools.langchain_sql_tool import query_ecommerce_database

load_dotenv()

# LLM using ChatGroq (Langchain_groq)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

tools = [query_ecommerce_database]

db = SQLDatabase.from_uri("sqlite:///data/ecommerce.db")

agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True
)