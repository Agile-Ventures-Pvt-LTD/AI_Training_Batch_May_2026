## MCP Tool Discovery
## Connects to all three local MCP servers over stdio and lists their tools.
## Writes the actual discovered tools to outputs/tool_discovery.json.
## No LLM involved — this only proves the servers are reachable and expose
## the expected tools.

from __future__ import annotations
import json
import asyncio
from pathlib import Path
from fastmcp import Client

try:
    PARENT_DIR = Path(__file__).resolve().parent
except NameError:
    PARENT_DIR = Path.cwd()

SERVERS = {
    "service-health": PARENT_DIR / "servers" / "service_health_server.py",
    "support-ticket": PARENT_DIR / "servers" / "support_ticket_server.py",
    "change-management": PARENT_DIR / "servers" / "change_management_server.py",
}

OUTPUT_PATH = PARENT_DIR / "outputs" / "tool_discovery.json"


async def discover_server_tools(server_path: Path) -> list[str]:
    """Connect to one local MCP server over stdio and return its tool names."""
    async with Client(str(server_path)) as client:
        tools = await client.list_tools()
        return [tool.name for tool in tools]


async def discover_all() -> dict[str, list[str]]:
    """Connect to each configured server in turn and collect discovered tools."""
    discovered: dict[str, list[str]] = {}

    for server_name, server_path in SERVERS.items():
        print(f"Connecting to {server_name}...")
        tool_names = await discover_server_tools(server_path)
        for name in tool_names:
            print(f"  - {name}")
        discovered[server_name] = tool_names

    return discovered


async def main() -> None:
    discovered = await discover_all()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(discovered, f, indent=2)

    print(f"\nWrote discovered tools to {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())