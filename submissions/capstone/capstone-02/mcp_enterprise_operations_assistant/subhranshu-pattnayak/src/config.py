"""Main Configuration file for MCP Host."""
import os, json
from dotenv import load_dotenv
from typing import Any
load_dotenv()


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, os.getenv("OUTPUT_PATH"))
SRC_PATH = os.path.join(ROOT_DIR, os.getenv("SRC_PATH"))
SERVER_PATH = os.path.join(ROOT_DIR, os.getenv("SERVER_PATH"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not in .env")


def read_json(file_path: str) -> dict[str, Any]:
    """Reads json files and return dict output."""
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found at: {file_path}")
