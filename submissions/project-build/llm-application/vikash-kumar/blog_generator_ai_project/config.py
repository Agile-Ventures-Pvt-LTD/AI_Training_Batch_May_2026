import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

DEFAULT_TEMPERATURE = 0.3
MAX_TOKENS = 3000
REQUEST_TIMEOUT = 60

SUPPORTED_LENGTHS = [
    "short",
    "medium",
    "long"
]