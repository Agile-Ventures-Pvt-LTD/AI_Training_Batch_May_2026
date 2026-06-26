import logging

from fastmcp import FastMCP

try:
    from src.prompts import register_prompts
    from src.resources import register_resources
    from src.tools import register_tools
except ModuleNotFoundError:
    from prompts import register_prompts
    from resources import register_resources
    from tools import register_tools

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

mcp = FastMCP("Weather Travel Advisory")

register_resources(mcp)
register_prompts(mcp)
register_tools(mcp)


if __name__ == "__main__":
    mcp.run()