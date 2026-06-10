from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_groq import ChatGroq

from src.tools.langchain_sql_tool import query_ecommerce_database
from src.prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

agent = create_agent(
    model=model,
    tools=[query_ecommerce_database],
    system_prompt=SYSTEM_PROMPT
)