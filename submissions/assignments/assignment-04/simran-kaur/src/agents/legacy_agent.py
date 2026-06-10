from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
    SystemMessage
)

from dotenv import load_dotenv
load_dotenv()

import os
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

from langchain_groq import ChatGroq

from src.tools.ecommerce_sql_tool import execute_sql
from src.prompts.system_prompt import SYSTEM_PROMPT


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ['GROQ_API_KEY'],
    temperature=0
)

available_tools = {
    "execute_sql": execute_sql
}

agent = llm.bind_tools(
    list(available_tools.values()),
    tool_choice="auto"
)


def run_agent(user_query: str):

    messages = [
        HumanMessage(content=user_query)
    ]

    first_response = agent.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages
        ]
    )

    messages.append(first_response)

    if first_response.tool_calls:

        for tool_call in first_response.tool_calls:

            tool_name = tool_call["name"]

            selected_tool = available_tools[
                tool_name
            ]

            tool_result = selected_tool.invoke(
                tool_call["args"]
            )

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )

    final_response = agent.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages
        ]
    )

    return final_response.content


if __name__ == "__main__":

    query = input("Ask a question: ")

    answer = run_agent(query)

    print("\nAnswer:\n")

    print(answer)


# run ```python -m src.agents.legacy_agent``` to execute