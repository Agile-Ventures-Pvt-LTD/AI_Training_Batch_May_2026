from pathlib import Path
import asyncio
import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool

from src.llm import groq_llm
from src.mcp_client import JiraMCPClient
from src.prompts import SYSTEM_PROMPT


class JiraHost:

    def __init__(self):
        self.client = JiraMCPClient()
        self.tools = []

    async def connect(self):
        """
        Connect to the MCP server and discover tools.
        """

        await self.client.connect()

        discovered_tools = await self.client.list_tools()

        self.tools = []

        for tool in discovered_tools:

            async def _tool_executor(
                _tool_name=tool.name,
                **kwargs
            ):
                result = await self.client.call_tool(
                    _tool_name,
                    kwargs,
                )

                return str(result)

            structured_tool = StructuredTool.from_function(
                coroutine=_tool_executor,
                name=tool.name,
                description=tool.description or "",
            )

            self.tools.append(structured_tool)

    async def chat(self, query: str):

        llm = groq_llm.bind_tools(self.tools)

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query),
        ]

        response = await llm.ainvoke(messages)

        tool_calls = getattr(response, "tool_calls", [])

        tools_used = []

        tool_outputs = []

        for call in tool_calls:

            tool_name = call["name"]

            args = call["args"]

            tools_used.append(tool_name)

            result = await self.client.call_tool(
                tool_name,
                args,
            )

            tool_outputs.append(
                {
                    "tool": tool_name,
                    "result": result,
                }
            )

        if tool_outputs:

            final_messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=f"""
User Query:
{query}

Tool Outputs:
{json.dumps(tool_outputs, indent=2, default=str)}

Generate the final answer.
"""
                ),
            ]

            final_response = await groq_llm.ainvoke(
                final_messages
            )

            return {
                "user_query": query,
                "tools_used": tools_used,
                "final_answer": final_response.content,
                "write_action_performed":
                    any(
                        tool in [
                            "add_issue_comment",
                            "update_issue_status",
                        ]
                        for tool in tools_used
                    ),
            }

        return {
            "user_query": query,
            "tools_used": [],
            "final_answer": response.content,
            "write_action_performed": False,
        }

    async def close(self):
        await self.client.disconnect()


async def main():

    host = JiraHost()

    await host.connect()

    print("=" * 70)
    print("Jira Issue Assistant")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:

        query = input("\nYou: ").strip()

        if query.lower() in ["exit", "quit"]:

            break

        response = await host.chat(query)
        
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        file_path = output_dir / "sample_outputs.json"


        if file_path.exists():

            existing_data = json.loads(file_path.read_text(encoding="utf-8"))
        else:
             existing_data = []

        existing_data.append(response)

        file_path.write_text(
        json.dumps(existing_data, indent=4, default=str),
        encoding="utf-8"
)

        print("\nAssistant\n")

        print(json.dumps(response, indent=4))

    await host.close()


if __name__ == "__main__":
    asyncio.run(main())
