from mcp_use import MCPClient
from pathlib import Path


try:
    PARENT_DIR = Path(__file__).resolve().parent
except NameError:
    PARENT_DIR = Path.cwd()

server_file = PARENT_DIR.parent / "server" / "jira_mcp_server.py"


config = MCPClient({
    "mcpServers": {
        "weather": {
            "command": "python",
            "args": [
                str(server_file)
            ]
        }
    }
})













