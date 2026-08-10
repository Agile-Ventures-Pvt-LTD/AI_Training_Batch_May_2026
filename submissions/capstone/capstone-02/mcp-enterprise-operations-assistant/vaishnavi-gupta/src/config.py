import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", ""),
    GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
    temperature = 0
)
)


