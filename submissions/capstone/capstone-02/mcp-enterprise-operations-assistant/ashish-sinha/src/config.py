import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR/"data"
TICKET_DB_PATH = DATA_DIR/"tickets.db"
SERVICE_HEALTH_JSON_PATH = DATA_DIR/"service_health.json"
CHANGE_PATH = DATA_DIR / "changes.json"

# MCP_SERVER_CONFIG = {
#     "mcpServers": {
#         "service-health": {
#             "command": "uv",
#             "args": [
#                 "run",
#                 "python",
#                 "servers/service_health_server.py"
#                 ]
#                 },
#             "support-ticket": {
#                 "command": "uv",
#                 "args": [
#                     "run",
#                     "python",
#                     "servers/support_ticket_server.py"
#                     ]
#                     },
#             "change-management": {
#                 "command": "uv",
#                 "args": [
#                     "run",
#                     "python",
#                     "servers/change_management_server.py"
#                 ]
#             }
#     }
# }

MCP_SERVER_CONFIG = {
    "mcpServers": {
        "service-health": {
            "command": "python",
            "args": [
                "-m",
                "servers.service_health_server"
                ]
                },
            "support-ticket": {
                "command": "python",
                "args": [
                    "-m",
                    "servers.support_ticket_server"
                    ]
                    },
            "change-management": {
                "command": "python",
                "args": [
                    "-m",
                    "servers.change_management_server"
                ]
            }
    }
}