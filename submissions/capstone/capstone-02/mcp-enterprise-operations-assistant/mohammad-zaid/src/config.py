import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

DATA_DIR = BASE_DIR / "data"
HEALTH_FILE = DATA_DIR / "service_health.json"
TICKETS_DB = DATA_DIR / "tickets.db"
CHANGES_FILE = DATA_DIR / "changes.json"
OUTPUT_DIR = BASE_DIR / "outputs"

SERVER_CONFIGS = {
    "mcpServers": {
        "service-health": {
            "command": "uv",
            "args": ["run", "python", str(BASE_DIR / "servers/service_health_server.py")],
        },
        "support-ticket": {
            "command": "uv",
            "args": ["run", "python", str(BASE_DIR / "servers/support_ticket_server.py")],
        },
        "change-management": {
            "command": "uv",
            "args": ["run", "python", str(BASE_DIR / "servers/change_management_server.py")],
        },
    }
}