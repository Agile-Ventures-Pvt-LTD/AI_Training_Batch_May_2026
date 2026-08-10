from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import os
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

# from langgraph.prebuilt import create_react_agent

from langchain.agents import create_agent

from src.tools.ecommerce_sql_tool import execute_sql
from src.prompts.system_prompt import SYSTEM_PROMPT


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ['GROQ_API_KEY'],
    temperature=0
)


agent = create_agent(
    model=llm,
    tools=[execute_sql],
    system_prompt=SYSTEM_PROMPT
)


def run_agent(user_query: str):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        }
    )

    return response["messages"][-1].content


if __name__ == "__main__":

    query = input("Ask a question: ")

    answer = run_agent(query)

    print("\nAnswer:\n")

    print(answer)

    # run ```python -m src.agents.modern_agent``` to execute
    
    #  Ask a question: Which customer has spent the most money?