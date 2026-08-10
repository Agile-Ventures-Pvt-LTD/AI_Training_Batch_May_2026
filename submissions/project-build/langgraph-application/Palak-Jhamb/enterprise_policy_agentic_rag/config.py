import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    try:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("API key not found")
        return key

    except Exception as e:
        print(f"API KEY not found: {e}")
        return None
    

CHUNK_SIZE = 900
CHUNK_OVERLAP = 120
DB_PATH = "vector_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3
folder_path ="data/policies"
