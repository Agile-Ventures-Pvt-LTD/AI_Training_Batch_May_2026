from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def getenv(key: str, default: Any = None) -> Any:
    return os.environ.get(key, default)

GROQ_API_KEY = getenv("GROQ_API_KEY", "")
GROQ_MODEL = getenv("GROQ_MODEL", "gpt-4o-mini")
DB_PATH = getenv("DB_PATH", os.path.join(BASE_DIR, "data", "database", "it_support.db"))
KB_PATH = getenv("KB_PATH", os.path.join(BASE_DIR, "data", "knowledge_base"))
VECTOR_STORE_PATH = getenv("VECTOR_STORE_PATH", os.path.join(BASE_DIR, "vector_store"))
EMBEDDING_MODEL = getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_SIZE = int(getenv("CHUNK_SIZE", 900))
CHUNK_OVERLAP = int(getenv("CHUNK_OVERLAP", 120))
TOP_K = int(getenv("TOP_K", 4))
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

GUIDE_DATA_PATH = os.getenv("GUIDE_DATA_PATH", "data/knowledge_base")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vector_store")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 900))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 120))
TOP_K = int(os.getenv("TOP_K", 4))