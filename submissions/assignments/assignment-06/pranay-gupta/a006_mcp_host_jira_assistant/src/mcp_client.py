import sys
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.exit_stack = AsyncExitStack()
        self.session = None
        self.tools = []

    async def connect(self):
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[self.server_script_path],
            env=None
        )
        read_stream, write_stream = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self.session.initialize()
        
        tools_response = await self.session.list_tools()
        self.tools = tools_response.tools
        return [tool.name for tool in self.tools]

    async def execute_tool(self, name: str, args: dict) -> str:
        if not self.session:
            raise RuntimeError("Client session not connected.")
        result = await self.session.call_tool(name, arguments=args)
        if result.content and len(result.content) > 0:
            return result.content[0].text
        return str(result)

    async def disconnect(self):
        await self.exit_stack.aclose()