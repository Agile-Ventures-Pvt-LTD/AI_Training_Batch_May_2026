from langchain.agents import AgentType,initialize_agent
from langchain_groq import ChatGroq

from config import GROQ_Model
from prompts import System_Prompt

from tools import get_tools

import os

def agent_build():
    llm = ChatGroq(api_key=os.environ['GROQ_API_KEY'],model=GROQ_Model,temperature=0)

    tools = get_tools()
    
    agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={
        "prefix": System_Prompt
    }
)

    return agent
