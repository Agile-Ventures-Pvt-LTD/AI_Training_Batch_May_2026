from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asyncio
import sys
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class JiraMCPClient:
    """
    Handles communication with the Jira MCP Server over stdio.
    """

    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.session: ClientSession | None = None

    async def connect(self):
        """
        Start the Jira MCP Server and initialize the MCP session.
        """

        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "server.jira_mcp_server"],
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
        Return all tools exposed by the MCP server.
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
    client = JiraMCPClient()

    await client.connect()

    tools = await client.list_tools()

    print("\nAvailable Tools:\n")

    for tool in tools:
        print(f"- {tool.name}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())