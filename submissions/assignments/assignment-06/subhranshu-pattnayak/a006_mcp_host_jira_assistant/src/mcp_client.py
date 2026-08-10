try:
    from src_config import SERVER_DIR
except ImportError:
    from .src_config import SERVER_DIR
from mcp_use import MCPClient
import os

server_file = os.path.join(SERVER_DIR, "jira_mcp_server.py")

def get_client():
    return MCPClient({
        "mcpServers": {
            "Jira MCP Server": {
                "command": "python",
                "args": [str(server_file)]
            }
        }
    })