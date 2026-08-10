import json
import asyncio
from pathlib import Path
from mcp_use import MCPClient
from src.config import MCP_SERVER_CONFIG

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "outputs" / "tool_discovery.json"

async def discover_tools():
    client = MCPClient(MCP_SERVER_CONFIG)
    await client.create_all_sessions()
    result = {}
    for server_name in MCP_SERVER_CONFIG["mcpServers"]:
        session = client.get_session(server_name)
        tools = await session.list_tools()
        result[server_name] = [t.name for t in tools]
    await client.close_all_sessions()
    return result

def run_discovery():
    result = asyncio.run(discover_tools())
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Tool discovery saved to {OUTPUT_PATH}")
    for server, tools in result.items():
        print(f"  {server}: {tools}")
    return result

if __name__ == "__main__":
    run_discovery()