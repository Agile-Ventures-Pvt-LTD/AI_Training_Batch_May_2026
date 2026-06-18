import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    """Central configuration for the application."""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    DB_PATH = os.getenv("DB_PATH", "data/ccms.db")

    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            print("WARNING: GROQ_API_KEY is not set. Please create a .env file and set it.")

config = Config()
config.validate()