from pathlib import Path
from mcp_use import MCPClient

ROOT_DIR = Path(__file__).resolve().parent.parent

available_tools = [
    "list_projects",
    "search_issues",
    "get_issue_details",
    "get_issue_comments",
    "add_issue_comment",
    "update_issue_status",
]

client = MCPClient(str(ROOT_DIR / "mcp.json"))
