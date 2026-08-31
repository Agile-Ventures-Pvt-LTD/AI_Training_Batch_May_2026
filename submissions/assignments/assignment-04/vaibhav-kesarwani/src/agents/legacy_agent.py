import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage
)
from src.tools.ecommerce_sql_tool import query_ecommerce_database
from src.prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0
)

tools = [query_ecommerce_database]

agent = llm.bind_tools(
    tools,
    tool_choice="auto"
)


def legacy_agent(question: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=question)
    ]

    max_iterations = 5

    for _ in range(max_iterations):
        response = agent.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # print(tool_call)

            try:
                if tool_name == "query_ecommerce_database":
                    result = query_ecommerce_database.invoke(tool_args)
                    # print("TOOL RESULT:", result)

                else:
                    result = f"Unknown tool: {tool_name}"

            except Exception as e:
                result = f"Tool execution error: {str(e)}"

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                    name=tool_name
                )
            )

    return "Unable to complete the request after multiple tool calls."