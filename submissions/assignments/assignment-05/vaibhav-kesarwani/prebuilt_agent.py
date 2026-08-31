from config import llm
from tools import prebuilt_tools
from prompts import system_prompt
from langgraph.prebuilt import create_react_agent

try:
    agent = create_react_agent(
        model = llm,
        tools=prebuilt_tools,
        prompt=system_prompt
    )
except Exception as e:
    print(e)