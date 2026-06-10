import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)

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

# Available tools
available_tools = {
    "query_ecommerce_database": query_ecommerce_database
}

# Bind tools to LLM
agent = llm.bind_tools(
    list(available_tools.values()),
    tool_choice="auto",
    parallel_tool_calls=True
)


def invoke(user_query: str):
    """
    Main agent execution function
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_query)
    ]

    # First LLM call
    response = agent.invoke(messages)
    messages.append(response)

    # If no tool call is required
    if not response.tool_calls:
        return response.content

    # Execute tool calls
    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]

        tool = available_tools[tool_name]

        tool_result = tool.invoke(tool_call["args"])

        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )

    # Second LLM call
    final_response = agent.invoke(messages)

    return final_response.content