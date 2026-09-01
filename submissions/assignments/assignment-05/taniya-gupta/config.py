import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.path.join("data","ccms.db")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"