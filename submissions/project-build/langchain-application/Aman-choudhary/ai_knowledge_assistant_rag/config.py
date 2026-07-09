import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Central configuration for the AI Knowledge Assistant RAG project."""
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data" / "raw"
    VECTOR_STORE_DIR = BASE_DIR / "data" / "vector_store"
    LOG_FILE_PATH = BASE_DIR / "logs" / "query_logs.jsonl"
    BENCHMARK_FILE_PATH = BASE_DIR / "outputs" / "benchmark_results.json"

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL_NAME = "llama-3.1-8b-instant"
    TEMPERATURE = 0.1
    MAX_TOKENS = 4096
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
if not Config.GROQ_API_KEY:
    raise ValueError("CRITICAL: GROQ_API_KEY is missing. Please check your .env file.")