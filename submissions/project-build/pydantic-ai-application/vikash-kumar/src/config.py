import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL","openai/gpt-oss-120b") #llama-3.3-70b-versatile
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
HF_TOKEN=os.getenv("HF_TOKEN")

MODEL_NAME="all-MiniLM-L6-v2"
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 900))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 120))
