import sys
import asyncio
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from src.prompts import SYSTEM_PROMPT
from langchain_groq import ChatGroq
from pathlib import Path
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
)

class GroqLLM:
    """
    Wrapper class for initializing the Groq LLM.
    """

    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=0,
        )

    def get_llm(self):
        """
        Return the initialized ChatGroq instance.
        """
        return self.llm

groq_llm = GroqLLM().get_llm()

###################################################################################

class MCPHost:

    def __init__(self):
        self.client = MCPClient()
        self.tools = []

    async def connect(self):
        """
        Connect to the MCP servers and discover tools.
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

    async def chat(self, user_query: str):

        llm = groq_llm.bind_tools(self.tools)

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_query),
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
{user_query}

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
                "user_query": user_query,
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
            "user_query": user_query,
            "tools_used": [],
            "final_answer": response.content,
            "write_action_performed": False,
        }

    async def close(self):
        await self.client.disconnect()


async def main():

    host = MCPHost()

    await host.connect()

    print("=" * 70)
    print("Enterprise Operations Assistant")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:

        user_query = input("\nYou: ").strip()

        if user_query.lower() in ["exit", "quit"]:

            break

        response = await host.chat(user_query)
        
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        file_path = output_dir / "sample_run_outputs.md"


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


################################################################################


class MCPClient:
    """
    Handles communication with the MCP Server over stdio.
    """

    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.session: ClientSession | None = None

    async def connect(self):
        """
        Start the MCP Servers and initialize the MCP session.
        """

        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "servers.support_ticket_server"],
                 ["-m", "servers.service_health_server"],
                 ["-m", "servers.change_management_server"]
)
        

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        read_stream, write_stream = stdio_transport

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        await self.session.initialize()

    async def disconnect(self):
        """
        Close the MCP session.
        """

        await self.exit_stack.aclose()

    async def list_tools(self):
        """
        Return all tools exposed by the MCP servers.
        """

        if self.session is None:
            raise RuntimeError("Client is not connected.")

        response = await self.session.list_tools()
        return response.tools

    async def call_tool(self, tool_name: str, arguments: dict):
        """
        Call a tool on the MCP server.
        """

        if self.session is None:
            raise RuntimeError("Client is not connected.")

        result = await self.session.call_tool(
            tool_name,
            arguments,
        )

        return result


# ------------------------------------------------------
# Demo
# ------------------------------------------------------

async def main():
    client = MCPClient()

    await client.connect()

    tools = await client.list_tools()

    print("\nAvailable Tools:\n")

    for tool in tools:
        print(f"- {tool.name}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())





