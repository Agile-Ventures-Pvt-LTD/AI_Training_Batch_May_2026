import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL","openai/gpt-oss-120b") #llama-3.3-70b-versatile
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")

KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH","data/knowledge_base")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH","vector_store")
DB_PATH = os.getenv("DB_PATH", "data/database/it_support.db")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 900))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 120))

TOP_K = int(os.getenv("TOP_K", 4))