import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME =  os.getenv("GROQ_MODEL")

DB_PATH = os.getenv("DB_PATH")

from pathlib import Path

BASE_DIR =  Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "outputs"



