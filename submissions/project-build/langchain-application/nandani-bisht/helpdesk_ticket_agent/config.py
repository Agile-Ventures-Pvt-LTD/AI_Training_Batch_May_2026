from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
db_value = os.getenv("DB_PATH")
if db_value:
    DB_PATH = (BASE_DIR / db_value).resolve()
else:
    DB_PATH = (DATA_DIR / "helpdesk_agent.db").resolve()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)


ALLOWED_STATUS = [
    "Open",
    "In Progress",
    "Pending",
    "Pending Customer Response",
    "Resolved",
    "Closed",
    "Escalated",
]


DEFAULT_SESSION_ID = "default"

REFERENCE_TIME = "2026-06-12 09:00:00"


def validate_environment():

    missing = []

    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")

    if missing:
        raise ValueError(
            f"Missing environment variables: {missing}"
        )

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database file not found: {DB_PATH}"
        )


def settings():

    return {
        "db_path": str(DB_PATH),
        "model": GROQ_MODEL,
        "reference_time": REFERENCE_TIME
    }