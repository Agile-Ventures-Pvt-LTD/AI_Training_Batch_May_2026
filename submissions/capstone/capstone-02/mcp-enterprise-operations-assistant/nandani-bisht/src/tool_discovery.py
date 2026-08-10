import asyncio
import json
from pathlib import Path
from mcp_use import MCPClient
from src.config import MCP_CONFIG

async def discover_tools() -> dict:
    """Connect to configured MCP servers and discover their exposed tools.
    
    Returns:
        A dictionary mapping server names to lists of discovered tool names.
    """
    client = MCPClient(MCP_CONFIG)
    try:
        await client.create_all_sessions()
        
        discovery_results = {server_name: [] for server_name in MCP_CONFIG["mcpServers"].keys()}
        
        search_result = await client.search_tools(detail_level="names")
        for tool in search_result.get("results", []):
            server = tool.get("server")
            name = tool.get("name")
            if server in discovery_results:
                discovery_results[server].append(name)
                

        for server in discovery_results:
            discovery_results[server] = sorted(discovery_results[server])
            
        return discovery_results
    finally:
        await client.close_all_sessions()

def run_discovery():
    """Run discovery and save output to outputs/tool_discovery.json."""
    results = asyncio.run(discover_tools())
    output_path = Path(__file__).resolve().parents[1] / "outputs" / "tool_discovery.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Tool discovery output written to {output_path}")

if __name__ == "__main__":
    run_discovery()
