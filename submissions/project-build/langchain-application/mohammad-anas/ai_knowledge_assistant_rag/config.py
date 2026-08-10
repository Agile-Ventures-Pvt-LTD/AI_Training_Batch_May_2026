import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    GROQ_API_KEY = os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
    GROQ_MODEL  = os.environ['GROQ_MODEL'] = os.getenv("GROQ_MODEL")
    EMBEDDING_MODEL = os.environ['EMBEDDING_MODEL'] = os.getenv("EMBEDDING_MODEL")

    VECTOR_DB_DIR = "./data/vector_db"
    RAW_DATA_DIR = "./data/raw"
    LOG_FILE = "./logs/query_logs.jsonl"

    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 150
    TOP_K = 5
