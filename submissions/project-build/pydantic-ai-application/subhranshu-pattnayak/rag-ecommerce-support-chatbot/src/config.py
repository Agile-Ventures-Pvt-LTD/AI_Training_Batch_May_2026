"""Main Configuration file for Rag Ecommerce Support Chatbot."""

import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, os.getenv("OUTPUT_PATH"))
DATA_DIR = os.path.join(ROOT_DIR, os.getenv("DATA_PATH"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
DB_PATH = "./seller_guide_db"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not in .env")