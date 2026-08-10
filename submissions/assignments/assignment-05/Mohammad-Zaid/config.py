# config.py

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL")

DB_PATH = BASE_DIR / "data" / "ccms.db"

OUTPUT_DIR = BASE_DIR / "outputs"