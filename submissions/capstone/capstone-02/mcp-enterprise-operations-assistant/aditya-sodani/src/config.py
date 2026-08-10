from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

SERVICE_HEALTH_FILE = DATA_DIR / "service_health.json"
CHANGE_FILE = DATA_DIR / "changes.json"
TICKET_DB = DATA_DIR / "tickets.db"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

MCP_CONFIG = {
        "mcpServers":{
            "service-health":{
                "command": "uv",
                "args": [
                      "run",
                      "python",
                      "-m",
                      "servers.service_health_server"
                ]
            },
            "support-ticket": {
                "command": "uv",
                "args": [
                      "run",
                      "python",
                      "-m",
                      "servers.support_ticket_server"
                ]
            },
            "change-management": {
                "command": "uv",
                "args": [
                      "run",
                      "python",
                      "-m",
                      "servers.change_management_server"
                ]
            }
        }
}



def validate_environment() -> None:
    """
    Validate required environment variables.
    """

    if not GROQ_API_KEY:
        raise EnvironmentError(
            "GROQ_API_KEY not found. Please configure your .env file."
        )