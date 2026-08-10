from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant"
)

TEMPERATURE = 0.3
MAX_TOKENS = 3000