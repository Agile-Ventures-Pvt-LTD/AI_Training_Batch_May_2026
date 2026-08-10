"""Main Configuration file for Jira MCP SRC."""

import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, os.getenv("OUTPUT_PATH"))
SERVER_DIR = os.path.join(ROOT_DIR, os.getenv("SERVER_PATH"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not in .env")