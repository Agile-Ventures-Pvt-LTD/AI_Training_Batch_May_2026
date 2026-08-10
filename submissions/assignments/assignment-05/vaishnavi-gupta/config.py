import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

DB_PATH = os.getenv(
    "DB_PATH",
    "data/ccms.db"
)

MAX_RESULTS = 50

if not GROQ_API_KEY:
    raise ValueError(
        "Your GROQ_API_KEY is missing. "
        "Please put and save it in your .env file."
    )