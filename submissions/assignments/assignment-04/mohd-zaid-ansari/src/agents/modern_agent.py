import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

from tools.sql_tool import query_database
from prompts.system_prompt import SYSTEM_PROMPT

from langchain.agents import create_agent

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[query_database],
    system_prompt=SYSTEM_PROMPT
)

def answer_business_question(question: str):

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

    messages = response["messages"]

    generated_sql = None
    database_result = None
    final_answer = None

    for msg in messages:

        if hasattr(msg, "tool_calls") and msg.tool_calls:
            generated_sql = msg.tool_calls[0]["args"]["query"]

        if msg.__class__.__name__ == "ToolMessage":
            database_result = msg.content

    final_answer = messages[-1].content

    return {
        "sql": generated_sql,
        "result": database_result,
        "answer": final_answer
    }