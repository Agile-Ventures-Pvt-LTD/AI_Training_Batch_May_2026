import os
from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

DB_PATH = os.getenv(
    "DB_PATH",
    r"C:\Users\Divya Khandelwal\Desktop\helpdesk_ticket_agent\data\helpdesk_agent_db_package\helpdesk_agent.db"
)


def validate_config():

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY missing. Please add it in .env file"
        )

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}"
        )

    return True