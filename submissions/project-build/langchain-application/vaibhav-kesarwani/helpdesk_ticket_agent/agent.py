import os
from dotenv import load_dotenv
from tools import tools 
from config import output_schema
from prompts import system_agent
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_community.utilities import SQLDatabase

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")

llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model=os.environ["GROQ_MODEL"],
    temperature=0
)

db = SQLDatabase.from_uri("sqlite:///data/helpdesk_agent.db")

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_agent,
)

def helpdesk_agent(question: str):
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

    output_schema(user_request=question, agent_response=result)

    return result["messages"][-1].content