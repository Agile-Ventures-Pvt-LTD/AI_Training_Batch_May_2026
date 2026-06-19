import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )

    GROQ_MODEL= os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )

    DB_PATH =os.getenv(
        "DB_PATH",
        "data/database"
    )

    EMBEDDING_MODEL= os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    VECTOR_STORE_PATH= os.getenv(
        "VECTOR_STORE_PATH",
        "vector_store"
    )

    CHUNK_SIZE=os.getenv(
        "CHUNK_SIZE",
        900
    )

    CHUNK_OVERLAP=os.getenv(
        "CHUNK_OVERLAP",
        120
    )

    TOP_K=os.getenv(
        "TOP_K",
        4
    )

    
settings = Settings()