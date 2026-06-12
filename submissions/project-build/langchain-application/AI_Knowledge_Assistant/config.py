import os
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", 150))
TOP_K = int(os.environ.get("TOP_K", 5))
DATA_RAW_DIR = os.environ.get("DATA_RAW_DIR", "data/raw")
VECTOR_STORE_DIR = os.environ.get("VECTOR_STORE_DIR", "data/vector_store")