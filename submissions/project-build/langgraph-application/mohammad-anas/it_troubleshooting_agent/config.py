import os
from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv("GROQ_MODEL",)


DB_PATH = os.getenv("DB_PATH")

KB_PATH = os.getenv("KB_PATH")

VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH")


EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))

CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))

TOP_K = int(os.getenv("TOP_K"))