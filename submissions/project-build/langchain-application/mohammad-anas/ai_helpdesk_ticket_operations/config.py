import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Please provide the api key")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
DB_PATH = os.getenv("DB_PATH", "data/helpdesk_agent.db")