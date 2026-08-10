from langchain_core.messages import (
    HumanMessage,
    ToolMessage
)

from database.db_tools import (
    execute_sql,
    get_schema
)

from groq_client import get_client

TOOLS = {
    "get_schema": get_schema,
    "execute_sql": execute_sql,
}

class SQLAgent:

    def __init__(self, model_name: str | None = None):
        self.llm_without_tools = get_client(model_name)
        self.llm = self.llm_without_tools.bind_tools(
            list(TOOLS.values())
        )

    def invoke(self, query: str):

        messages = [
            HumanMessage(query)
        ]

        while True:

            ai_msg = self.llm.invoke(messages)
            messages.append(ai_msg)

            if not ai_msg.tool_calls:
                return ai_msg

            for tool_call in ai_msg.tool_calls:

                tool = TOOLS[
                    tool_call["name"].lower()
                ]

                output = tool.invoke(
                    tool_call["args"]
                )

                messages.append(
                    ToolMessage(
                        output,
                        tool_call_id=tool_call["id"]
                    )
                )