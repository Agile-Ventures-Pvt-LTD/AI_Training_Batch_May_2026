from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

class Settings:

    BASE_DIR = Path(__file__).parent

    RAW_DATA_DIR = BASE_DIR / "data" / "raw"

    PROCESSED_DIR = BASE_DIR / "data" / "processed"

    VECTOR_DB_DIR = BASE_DIR / "data" / "vector_store"

    LOG_DIR = BASE_DIR / "logs"

    OUTPUT_DIR = BASE_DIR / "outputs"

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    VECTOR_DB = os.getenv(
        "VECTOR_DB",
        "chroma"
    )

    CHUNK_SIZE = int(
        os.getenv("CHUNK_SIZE", 1000)
    )

    CHUNK_OVERLAP = int(
        os.getenv("CHUNK_OVERLAP", 150)
    )

    TOP_K = int(
        os.getenv("TOP_K", 5)
    )


settings = Settings()