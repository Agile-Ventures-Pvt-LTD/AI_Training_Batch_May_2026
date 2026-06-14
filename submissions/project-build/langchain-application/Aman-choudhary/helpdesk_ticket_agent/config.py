from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

DB_PATH = os.getenv(
    "DB_PATH",
    "data/helpdesk_agent_db_package/helpdesk_agent.db"
)