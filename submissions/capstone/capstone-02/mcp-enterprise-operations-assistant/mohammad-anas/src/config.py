import os
from dotenv import load_dotenv
load_dotenv()

DB_PATH = os.environ['DB_PATH'] = os.getenv("DB_PATH")

MCP_SERVER_CONFIG = {
    "mcpServers": {
        "service-health": {
            "command": "uv",
            "args": ["run", "python", "servers/service_health_server.py"]
        },
        "support-ticket": {
            "command": "uv",
            "args": ["run", "python", "servers/support_ticket_server.py"]
        },
        "change-management": {
            "command": "uv",
            "args": ["run", "python","servers/change_management_server.py"]
        }
    }
}