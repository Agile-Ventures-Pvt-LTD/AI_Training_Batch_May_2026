from dotenv import load_dotenv
import os
from pathlib import Path



load_dotenv()




BASE_DIR = Path(__file__).resolve().parent



GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)



DB_PATH = os.getenv(
    "DB_PATH",
    str(
        BASE_DIR
        / "data"
        / "helpdesk_agent_db_package"
        / "helpdesk_agent.db"
    )
)


# VALID TICKET STATUSES


VALID_STATUSES = [
    "Open",
    "In Progress",
    "Pending",
    "Resolved",
    "Closed",
    "Escalated"
]


# VALIDATION


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env"
    )



print("\nUsing Database:")
print(DB_PATH)
print()