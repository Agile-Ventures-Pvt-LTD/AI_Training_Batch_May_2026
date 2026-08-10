from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

DB_PATH = os.getenv(
    "DB_PATH",
    str(BASE_DIR / "data" / "helpdesk_agent.db")
)

DEBUG_MODE = os.getenv(
    "DEBUG_MODE",
    "False"
).lower() == "true"

SESSION_ID = os.getenv(
    "SESSION_ID",
    "default_session"
)


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in environment variables."
    )

if not Path(DB_PATH).exists():
    raise FileNotFoundError(
        f"Database not found: {DB_PATH}"
    )


ALLOWED_STATUSES = {
    "Open",
    "In Progress",
    "Pending",
    "Resolved",
    "Closed",
    "Escalated"
}


REFERENCE_TIME = "2026-06-12 12:00:00"



PRIORITY_SCORES = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Urgent": 4
}

CUSTOMER_TIER_SCORES = {
    "Standard": 1,
    "Premium": 2,
    "Enterprise": 3
}