import sys
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from config import GROQ_API_KEY, GROQ_MODEL
from prompts import SYSTEM_PROMPT
from tools import get_all_tools


def test_agent():
    llm = ChatGroq(api_key=GROQ_API_KEY,model=GROQ_MODEL,temperature=0.7,timeout=30)
    tools = get_all_tools()
    for tool in tools:
        print(f"  - {tool}")
    try:
        agent = create_react_agent(
            model=llm,
            tools=tools
        )
    except Exception as e:
        print(f"Error{e}")
        return False

    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content="What is 2+2?")
        ]
        
        result = agent.invoke({
            "messages": messages
        })
        print(f"  Result type: {type(result)}")
        print(f"  Result keys: {result.keys() if isinstance(result, dict) else 'N/A'}")
        
        return True
    
    except Exception as e:
        print(f"Error{e}")
        return False


if __name__ == "__main__":
    success = test_agent()
    
