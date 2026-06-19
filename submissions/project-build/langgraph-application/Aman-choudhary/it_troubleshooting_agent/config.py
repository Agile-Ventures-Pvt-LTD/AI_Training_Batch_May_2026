import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")
DB_PATH = os.getenv("DB_PATH")
KB_PATH = os.getenv("KB_PATH")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH","vector_store")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", 4))