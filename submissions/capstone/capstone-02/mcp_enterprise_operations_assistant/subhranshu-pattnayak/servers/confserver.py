"""Main Configuration file for MCP Servers."""
import sqlite3
import os, json
from dotenv import load_dotenv
from typing import Any
load_dotenv()


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, os.getenv("OUTPUT_PATH"))
DATA_DIR = os.path.join(ROOT_DIR, os.getenv("DATA_PATH"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

TICKET_PATH = os.path.join(DATA_DIR, os.getenv("tickets"))
SERVICE_HEALTH_PATH = os.path.join(DATA_DIR, os.getenv("service_health"))
CHANGES_MANAGEMENT_PATH = os.path.join(DATA_DIR, os.getenv("changes"))

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not in .env")


def read_json(file_path: str) -> dict[str, Any]:
    """Reads json files and return dict output."""
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found at: {file_path}")

def get_conn():
    """Provides database connection."""
    try:
        return sqlite3.connect(TICKET_PATH)
    except Exception as e:
        print(f"Database connection Error: {str(e)}")