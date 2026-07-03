from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama-3.3-70b-versatile"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)


BASE_DIR = Path(__file__).parent

DATA_PATH = Path(
    os.getenv(
        "DATA_PATH",
        "data/seller_guide.pdf"
    )
)

VECTOR_DB_PATH = Path(
    os.getenv(
        "VECTOR_DB_PATH",
        "chroma_db"
    )
)

OUTPUT_PATH = BASE_DIR / "outputs"


CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", 1000)
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", 150)
)


TOP_K = int(
    os.getenv("TOP_K", 4)
)
