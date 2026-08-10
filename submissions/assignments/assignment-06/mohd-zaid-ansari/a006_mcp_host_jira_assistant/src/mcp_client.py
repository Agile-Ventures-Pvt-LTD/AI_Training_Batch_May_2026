from pathlib import Path
from mcp_use import MCPClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SERVER_PATH = PROJECT_ROOT / "server" / "jira_mcp_server.py"

def mcp_client():
    config=MCPClient({
        "mcpServers":{
            "jira":{
                "command":"python",
                "args":[str(SERVER_PATH)]
            }
        }
    })
    return config
