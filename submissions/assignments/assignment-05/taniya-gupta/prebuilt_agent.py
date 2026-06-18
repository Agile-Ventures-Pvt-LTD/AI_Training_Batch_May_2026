from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from config import GROQ_API_KEY, MODEL_NAME
from tools import TOOLS
from prompts import SYSTEM_PROMPT

llm = ChatGroq(model=MODEL_NAME, temperature=0, api_key=GROQ_API_KEY, max_retries=2)
agent = create_react_agent(llm, tools=TOOLS, prompt=SYSTEM_PROMPT)

def run_prebuilt_agent(question):
    """Executes the pre-built agent"""
    result = agent.invoke({"messages": [("human", question)]}, config={"recursion_limit": 10})
    return result
