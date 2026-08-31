import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from src.prompts.system_prompt import SYSTEM_PROMPT
from langchain_community.utilities import SQLDatabase
from src.tools.ecommerce_sql_tool import query_ecommerce_database
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from src.db.connection import get_connection

load_dotenv()

llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model="openai/gpt-oss-120b",
    temperature=0
)

db = SQLDatabase.from_uri("sqlite:///data/ecommerce.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

def modern_agent(question: str):
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    return result["messages"][-1].content