import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Project Paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data" 
    VECTOR_STORE_DIR = BASE_DIR / "chroma_db"


    # Groq & LLM Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL_NAME = "llama-3.3-70b-versatile"
    TEMPERATURE = 0.1
    MAX_TOKENS = 4096

    # Embeddings & Vector Store Configuration
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    # RAG Splitter Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

if not Config.GROQ_API_KEY:
    raise ValueError("CRITICAL: GROQ_API_KEY is missing. Please check your .env file.")