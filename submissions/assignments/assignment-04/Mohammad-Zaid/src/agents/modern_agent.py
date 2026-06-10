# src/agents/modern_agent.py
# langchain >= 1.3.6

from dotenv import load_dotenv

from langchain.agents import create_agent

from langchain_groq import ChatGroq

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)

from src.prompts.system_prompt import (
    SYSTEM_PROMPT
)


load_dotenv()

# LLM

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Tools

tools = [query_ecommerce_database]

# Modern Agent

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)


def ask_agent(question: str):
    """
    Modern LangChain Agent Interface
    """

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    return (
        response["messages"][1].tool_calls[0]["args"]["sql_query"],
        response["messages"][-1].content
    )