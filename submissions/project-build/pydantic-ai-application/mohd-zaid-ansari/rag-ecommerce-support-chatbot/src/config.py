import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
MODEL=os.getenv('GROQ_MODEL')
HF_TOKEN=os.getenv("HF_TOKEN")

EMBEDDING_MODEL="sentence-transformers/all-mpnet-base-v2" 
DATASET_PATH="data"
VECTORE_STORE_PATH="chroma_db"

CHUNK_SIZE=400
CHUNK_OVERLAP=50
TOP_K=3