import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN=os.getenv("HF_TOKEN")

MODEL_NAME =  os.getenv("GROQ_MODEL")


DB_PATH="data/database/it_support.db"
KB_PATH="data/knowledge_base"
VECTOR_STORE_PATH="vector_store"
EMBEDDING_MODEL="sentence-transformers/all-mpnet-base-v2" 
CHUNK_SIZE=900
CHUNK_OVERLAP=120
TOP_K=4