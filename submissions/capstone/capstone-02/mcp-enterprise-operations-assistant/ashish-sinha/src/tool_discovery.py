import asyncio
from mcp_use import MCPClient
from src.config import MCP_SERVER_CONFIG
from src.output_writer import write_tool_discovery

async def generate_mcp_schema_snapshot() -> None:
    client = MCPClient(MCP_SERVER_CONFIG)
    schema_map = {}
    await client.initialize()
    for server_name, connection in client.servers.items():
        discovered_tools = await connection.list_tools()
        schema_map[server_name] = [tool.name for tool in discovered_tools]
    write_tool_discovery(schema_map)

if __name__ == "__main__":
    asyncio.run(generate_mcp_schema_snapshot())


