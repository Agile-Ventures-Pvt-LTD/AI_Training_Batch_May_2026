from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv("GROQ_MODEL")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 900))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 120))

TOP_K = int(os.getenv("TOP_K", 4))

KB_PATH = os.getenv("KB_PATH")

DB_PATH = os.getenv("DB_PATH")

VECTOR_DB_PATH = os.getenv("VECTOR_STORE_PATH")

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
