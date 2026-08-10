import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
DATA_ROOT = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_ROOT / "raw"
PROCESSED_DIR = DATA_ROOT / "processed"
VECTOR_STORE_DIR = DATA_ROOT / "vector_store"
LOGS_DIR = ROOT_DIR / "logs"
OUTPUTS_DIR = ROOT_DIR / "outputs"

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
TOP_K = int(os.getenv("TOP_K", "5"))
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
VECTOR_DB = os.getenv("VECTOR_DB", "chroma")

QUERY_LOG_FILE = LOGS_DIR / "query_logs.jsonl"
BENCHMARK_OUTPUT_FILE = OUTPUTS_DIR / "benchmark_results.json"

SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".md"]
