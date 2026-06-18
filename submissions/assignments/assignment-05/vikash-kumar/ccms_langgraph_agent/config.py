import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/ccms.db")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

def get_llm():
    """
    Returns configured Groq LLM instance.
    """
    return ChatGroq(
        model=GROQ_MODEL,
        groq_api_key=GROQ_API_KEY,
        temperature=0)