import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from src.prompts.system_prompt import SYSTEM_PROMPT
from src.tools.ecommerce_sql_tool import query_ecommerce_database

# Load env
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


agent = create_agent(
    model=llm,
    tools=[query_ecommerce_database],
    system_prompt=SYSTEM_PROMPT
)


def invoke(question: str) -> str:
    """
    Invoke the modern LangChain agent.
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

    return response["messages"][-1].content
