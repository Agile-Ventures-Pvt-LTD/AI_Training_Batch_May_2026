
from typing import Optional
from contextlib import AsyncExitStack
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from groq import Groq
# from anthropic import Anthropic
from dotenv import load_dotenv
from src.output_writer import save_output

load_dotenv()  

class MCPClient:
    def __init__(self):
        
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.groq = Groq()



    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

    Args:
        server_script_path: Path to the server script (.py or .js)
    """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        tools_list=[]
        for tool in tools:
            tool_dict={
                "tool":tool.name,
                "tool_disc":tool.description
            }
            tools_list.append(tool_dict)
        print("\nConnected to server with tools:", [tool.name for tool in tools])
        return tools_list

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

import json
from pathlib import Path
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "outputs" / "tool_discovery.json"


def save_output(output: dict):

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(output)

    with open(OUTPUT_FILE, "w") as file:
        json.dump(data, file, indent=4)

       
async def main():
    client = MCPClient()
    try:
        # server_path=[
        #     "servers/service_health_server.py",
        #     "servers/support_ticket_server.py",
        #     "servers/change_management_server.py"
        # ]
        tools=await client.connect_to_server(sys.argv[1])
        save_output(tools)
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


# run : uv run -m src.tool_discovery servers/change_management_server.py