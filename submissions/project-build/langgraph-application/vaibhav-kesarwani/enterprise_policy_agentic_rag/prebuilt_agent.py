from config import llm
from tools import tools
from prompts import system_prompt
from langgraph.prebuilt import create_react_agent

try:
    agent = create_react_agent(
        model = llm,
        tools=tools,
        prompt=system_prompt
    )
except Exception as e:
    print(e)