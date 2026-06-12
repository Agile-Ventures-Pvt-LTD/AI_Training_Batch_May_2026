import os

from dotenv import load_dotenv

from prompts import SYSTEM_PROMPT


def build_agent():
    load_dotenv()

    try:
        from langchain.agents import create_agent
        from langchain_groq import ChatGroq
        from tools import TOOLS
        
    except ImportError as error:
        raise RuntimeError("Missing packages. Run: pip install -r requirements.txt") from error

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from your .env file.")

    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    llm = ChatGroq(model=model_name, api_key=api_key, temperature=0)

    return create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )

    

def run_agent(question):
    agent = build_agent()
    response = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return response["messages"][-1].content


def run_agent_with_response(question):
    agent = build_agent()
    response = agent.invoke({"messages": [{"role": "user", "content": question}]})
    answer = response["messages"][-1].content
    return answer, response
