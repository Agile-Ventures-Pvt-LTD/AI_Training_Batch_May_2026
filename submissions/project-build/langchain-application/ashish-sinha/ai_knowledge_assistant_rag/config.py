import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL","llama-3.3-70b-versatile"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2"
)

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", 1024)
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", 150)
)

TOP_K = int(
    os.getenv("TOP_K", 5)
)

RERANK_TOP_K = int(
    os.getenv("RERANK_TOP_K", 3)
)

VECTOR_DB_PATH = "data/vector_store"

RAW_DATA_PATH = "data/raw"

LOG_FILE = "logs/query_logs.jsonl"