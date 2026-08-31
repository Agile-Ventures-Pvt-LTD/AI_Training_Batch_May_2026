from dotenv import load_dotenv
import os

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)


CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))


TOP_K = int(os.getenv("TOP_K", 5))


RAW_DATA_PATH = "data/raw"

PROCESSED_DATA_PATH = "data/processed"

VECTOR_DB_PATH = "data/vector_store"

LOG_PATH = "logs/query_logs.jsonl"

BENCHMARK_OUTPUT = "outputs/benchmark_results.json"