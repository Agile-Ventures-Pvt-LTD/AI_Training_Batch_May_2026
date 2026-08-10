import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL")

def get_llm():
    llm=ChatGroq(
        model=MODEL_NAME
    )
    return llm