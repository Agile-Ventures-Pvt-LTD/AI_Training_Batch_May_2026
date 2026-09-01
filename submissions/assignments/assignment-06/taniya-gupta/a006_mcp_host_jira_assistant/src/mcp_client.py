import sys
from mcp_use import MCPClient

def get_client():
    config={
        "mcpServers": {
            "jira": {
                "command": sys.executable,
                "args": ["server/jira_mcp_server.py"]
            }
        }
    }

    return MCPClient.from_dict(config)