from typing import List, Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from config import llm
from tools import Tools
from prompts import System_Prompt

agent_executor = create_react_agent(
            model=llm,
            tools=Tools,
            prompt=System_Prompt
        )
