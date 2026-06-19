from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from config import GROQ_API_KEY, GROQ_MODEL
from prompts import SYSTEM_PROMPT
from tools import get_all_tools


def build_agent():
    llm = ChatGroq(api_key=GROQ_API_KEY,model=GROQ_MODEL,temperature=0.7,timeout=30)
    tools = get_all_tools()
    agent = create_react_agent(model=llm,tools=tools)
    return agent


def invoke_agent(agent_executor, query):
    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query)
        ]
        result = agent_executor.invoke({
            "messages": messages
        })
        return result
    except Exception as e:
        raise Exception(f"Agent invocation failed: {str(e)}")


def get_agent_state(agent_executor):
    tool_list = get_all_tools()
    return {
        "model": GROQ_MODEL,
        "system_prompt": SYSTEM_PROMPT[:100] + "...",
        "tools_count": len(tool_list),
        "tools": [tool.name for tool in tool_list]
    }
