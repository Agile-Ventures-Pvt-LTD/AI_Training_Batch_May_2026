import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / os.getenv("DATASET_PATH")

OUTPUT_PATH = BASE_DIR / os.getenv("OUTPUT_PATH")

LOG_PATH = BASE_DIR / os.getenv("LOG_PATH")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv("GROQ_MODEL")

TEMPERATURE = float(os.getenv("TEMPERATURE"))