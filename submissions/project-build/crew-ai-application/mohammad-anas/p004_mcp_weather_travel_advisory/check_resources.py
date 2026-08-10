import asyncio

from fastmcp import FastMCP
from src.resources import register_resources


async def main():
    mcp = FastMCP("Test")
    register_resources(mcp)

    print(await mcp.list_resources())


asyncio.run(main())