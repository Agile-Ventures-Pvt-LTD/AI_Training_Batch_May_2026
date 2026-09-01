import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")
    DB_PATH=os.getenv("DB_PATH")
    MAX_RESULTS = 5
    TRUNCATE_CHARS = 150