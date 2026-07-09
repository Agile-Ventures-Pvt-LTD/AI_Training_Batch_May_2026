from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")
MCP_CONFIG = {
    "mcpServers": {
        "service-health": {
            "command": "uv",
            "args": ["run",
                "python","servers/service_health_server.py",],
        },
        "support-ticket": {
            "command": "uv",
            "args": [
                "run",
                "python",
                "servers/support_ticket_server.py",],
        },
        "change-management": {
            "command": "uv",
            "args": [
                "run",
                "python",
                "servers/change_management_server.py",],},}}