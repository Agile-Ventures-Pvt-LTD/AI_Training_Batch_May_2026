import asyncio

from fastmcp import FastMCP
from src.prompts import register_prompts


async def main():
    mcp = FastMCP("Test")
    register_prompts(mcp)

    print(await mcp.list_prompts())


asyncio.run(main())