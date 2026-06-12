import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
    GROQ_MODEL=os.getenv("GROQ_MODEL")
    EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL")
    VECTOR_DB_DIR=os.getenv("VECTOR_DB_DIR")
    CHUNK_SIZE=int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP=int(os.getenv("CHUNK_OVERLAP", 150))
    TOP_K=int(os.getenv("TOP_K", 5))
    RAW_DATA_DIR="data/raw"
    LOG_FILE="logs/query_logs.jsonl"
    BENCHMARK_OUTPUT ="outputs/benchmark_results.json"
