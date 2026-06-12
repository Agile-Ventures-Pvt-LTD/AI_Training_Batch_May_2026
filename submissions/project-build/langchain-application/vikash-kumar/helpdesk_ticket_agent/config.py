import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "data" / "helpdesk_agent.db"

OUTPUT_DIR = BASE_DIR / "outputs"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME","openai/gpt-oss-120b")

MAX_CHAT_HISTORY = 10


ALLOWED_STATUSES = [
    "Open",
    "In Progress",
    "Pending Customer",
    "Resolved",
    "Closed"]


ALLOWED_PRIORITIES = [
    "Low",
    "Medium",
    "High",
    "Critical"]