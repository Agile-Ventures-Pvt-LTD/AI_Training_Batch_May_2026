# src/server.py
import json
import os
from fastmcp import FastMCP
from pathlib import Path
from dotenv import load_dotenv
from tools import register_tools
from resources import register_resources
from prompts import register_prompts
from report_writer import save_advisory_report

load_dotenv()
mcp = FastMCP("Travel Weather Advisor")

register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)

@mcp.tool(description="Saves the final advisory report as JSON to the outputs folder.")
async def save_travel_advisory_tool(report: dict) -> dict:
    try:
        file_path = save_advisory_report(report)
        return {"success": True, "saved_path": file_path}
    except Exception as e:
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")