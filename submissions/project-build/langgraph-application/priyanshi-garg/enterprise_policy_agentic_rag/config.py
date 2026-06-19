from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

CHUNK_SIZE = 900
CHUNK_OVERLAP = 120
TOP_K = 4

POLICY_DATA_PATH = "data/policies"
VECTOR_STORE_PATH = "vector_store"