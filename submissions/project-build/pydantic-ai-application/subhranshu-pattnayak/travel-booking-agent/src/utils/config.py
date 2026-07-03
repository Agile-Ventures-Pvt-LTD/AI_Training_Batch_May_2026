"""Main Configuration file for Rag Ecommerce Support Chatbot."""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(ROOT_DIR, os.getenv("SRC_PATH"))
UTILS_DIR = os.path.join(SRC_DIR, os.getenv("UTILS_PATH"))
OUTPUT_DIR = os.path.join(ROOT_DIR, os.getenv("OUTPUT_PATH"))
DATA_DIR = os.path.join(ROOT_DIR, os.getenv("DATA_PATH"))

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env")