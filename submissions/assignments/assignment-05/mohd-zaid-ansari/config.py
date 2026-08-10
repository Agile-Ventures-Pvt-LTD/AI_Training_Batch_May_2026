from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

db_path="data/ccms.db"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME =  os.getenv("GROQ_MODEL")