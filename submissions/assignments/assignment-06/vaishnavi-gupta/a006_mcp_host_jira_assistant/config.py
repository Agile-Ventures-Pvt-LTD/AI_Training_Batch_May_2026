from pathlib import Path

from dotenv import load_dotenv
import os

# --------------------------------------------------
# Load .env
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# Groq Configuration
# --------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

# --------------------------------------------------
# Jira Configuration
# --------------------------------------------------

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")

# --------------------------------------------------
# Logging
# --------------------------------------------------

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# --------------------------------------------------
# Validation
# --------------------------------------------------

REQUIRED_ENV_VARS = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "JIRA_BASE_URL": JIRA_BASE_URL,
    "JIRA_EMAIL": JIRA_EMAIL,
    "JIRA_API_TOKEN": JIRA_API_TOKEN,
}


def validate_env() -> None:
    """
    Validate required environment variables.
    """

    missing = [
        key
        for key, value in REQUIRED_ENV_VARS.items()
        if not value
    ]

    if missing:
        raise EnvironmentError(
            "Missing required environment variables:\n"
            + "\n".join(missing)
        )