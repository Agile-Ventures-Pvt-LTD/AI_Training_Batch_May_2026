import json 
import requests
from typing import List, Dict, Optional 
from fastmcp import FastMCP
from pathlib import Path
import os
from dotenv import load_dotenv
import tools
import resources
import src.prompts

BASE_DIR = Path(__file__).parent.resolve()


PARENT_DIR = BASE_DIR.parent
load_dotenv(dotenv_path=PARENT_DIR / ".env")

mcp = FastMCP("Weather Advisor")

if __name__ == "__main__":
    # mcp.run(transport="streamable-http")
    mcp.run(transport="stdio")


