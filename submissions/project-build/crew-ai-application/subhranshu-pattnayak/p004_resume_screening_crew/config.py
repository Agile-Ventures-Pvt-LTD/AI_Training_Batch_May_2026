import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent


DATASET_PATH = ROOT_DIR / os.getenv("DATASET_PATH")
METADATA_PATH = ROOT_DIR / os.getenv("DATASET_PATH") / "metadata"
OUTPUT_DIR = ROOT_DIR / os.getenv("OUTPUT_PATH")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not in .env")