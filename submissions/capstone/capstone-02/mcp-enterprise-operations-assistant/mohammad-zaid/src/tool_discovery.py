import asyncio
import sys
from pathlib import Path
from mcp_use import MCPClient

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import SERVER_CONFIGS
from src.output_writer import save_tool_discovery


async def generate_discovery() -> dict:

    print("Initializing dynamic MCP Server tool discovery...")
    client = MCPClient.from_dict(SERVER_CONFIGS)
    discovery = {}

    try:
        await client.create_all_sessions()
        for server_name in SERVER_CONFIGS["mcpServers"].keys():
            try:
                session = client.get_session(server_name)
                tools = await session.list_tools()
                discovery[server_name] = [t.name for t in tools]
            except Exception as e:
                print(f"Skipped {server_name} discovery : {e}")
                discovery[server_name] = []
    finally:
        await client.close_all_sessions()

    save_tool_discovery(discovery)
    print("Generated Server-Tool map.")
    return discovery


if __name__ == "__main__":
    asyncio.run(generate_discovery())