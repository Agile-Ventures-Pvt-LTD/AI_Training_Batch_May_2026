import asyncio
from mcp_use.client import MCPClient


CONFIG = {
    "mcpServers": {
        "jira": {
            "command": "python",
            "args": [
                "-m",
                "server.jira_mcp_server"
                ],
        }
    }
}


async def main():

    client = MCPClient.from_dict(CONFIG)

    print("Creating MCP sessions")
    await client.create_all_sessions()

    print("\nSearching tools\n")

    tools = await client.search_tools("")

    print("Available Tools:\n")

    tool_names = [tool["name"] for tool in tools["results"]]

    print(tool_names)

    await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(main())