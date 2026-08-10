
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Validate and load environment variables (from notebook)
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY Error:")

os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")
if not os.getenv("GROQ_MODEL"):
    raise ValueError("GROQ_MODEL Error:")

os.environ["EMBEDDING_MODEL"] = os.getenv("EMBEDDING_MODEL")
if not os.getenv("EMBEDDING_MODEL"):
    raise ValueError("EMBEDDING_MODEL Error:")

os.environ["VECTOR_DB"] = os.getenv("VECTOR_DB")
if not os.getenv("VECTOR_DB"):
    raise ValueError("VECTOR_DB Error:")

os.environ["CHUNK_SIZE"] = os.getenv("CHUNK_SIZE")
if not os.getenv("CHUNK_SIZE"):
    raise ValueError("CHUNK_SIZE Error:")

os.environ["CHUNK_OVERLAP"] = os.getenv("CHUNK_OVERLAP")
if not os.getenv("CHUNK_OVERLAP"):
    raise ValueError("CHUNK_OVERLAP Error:")

os.environ["TOP_K"] = os.getenv("TOP_K")
if not os.getenv("TOP_K"):
    raise ValueError("TOP_K Error:")

print("All environment variables loaded successfully.")
