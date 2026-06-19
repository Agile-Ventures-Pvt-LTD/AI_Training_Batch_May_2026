import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    GROQ_MODEL=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    DATA_PATH=os.getenv("DATA_PATH","data/policies")
    VECTOR_PATH=os.getenv("VECTOR_PATH", "vector_store")
    CHUNK_SIZE=os.getenv("CHUNK_SIZE",900)
    CHUNK_OVERLAP=os.getenv("CHUNK_OVERLAP",120)
    TOP_K=os.getenv("TOP_K",4)

config=Config()