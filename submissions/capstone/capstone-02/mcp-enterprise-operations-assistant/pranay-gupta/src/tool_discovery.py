import asyncio
from mcp_use import MCPClient
from src.config import MCP_SERVER_CONFIG
from src.output_writer import write_tool_discovery

async def discover_tools():
    client = MCPClient(MCP_SERVER_CONFIG)
    discovered = {}
    
    try:
        for server_name in MCP_SERVER_CONFIG["mcpServers"].keys():
            session = await client.create_session(server_name)
            await session.connect()
            tools = await session.list_tools()
            discovered[server_name] = [tool.name for tool in tools]
            
        write_tool_discovery(discovered)
        return discovered
    except Exception as e:
        raise
    finally:
        try:
            await client.close_all_sessions()
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(discover_tools())
