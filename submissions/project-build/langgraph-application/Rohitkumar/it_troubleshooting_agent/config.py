import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-mpnet-base-v2")
KB_DATA_PATH = os.getenv("KB_DATA_PATH", "data/knowledge_base")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vector_store")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
TOP_K = int(os.getenv("TOP_K", "4"))
DB_PATH = os.getenv(
    "DB_PATH",
    "data/ccms.db"
)

