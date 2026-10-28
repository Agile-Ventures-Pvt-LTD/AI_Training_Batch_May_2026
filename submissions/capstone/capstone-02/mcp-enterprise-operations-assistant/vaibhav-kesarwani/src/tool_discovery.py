import json
import os
import asyncio
from fastmcp import Client

MCP_FILE = "./src/mcp.json"
OUTPUT_FILE = os.path.join("outputs", "tools_discovery.json")

async def fetch_tools(server_name, server_info):
    script_path = server_info["args"][0]
    
    try:
        async with Client(script_path) as client:
            tools = await client.list_tools()
            
            print(f"{server_name}: {len(tools)} tools found")
            
            return {"server": server_name, "tools": [t.name for t in tools]}
    
    except Exception as e:
        print(f"{server_name} failed: {e}")


async def tool_discovery():
    with open(MCP_FILE, "r") as f:
        data = json.load(f)

    os.makedirs("outputs", exist_ok=True)

    tasks = [
        fetch_tools(server_name, server_info)
        for server_name, server_info in data["mcpServers"].items()
    ]
    results = await asyncio.gather(*tasks)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(tool_discovery())
