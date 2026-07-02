import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_groq_llm():
    """Initialize and return a Groq LLM instance using langchain-groq ChatGroq."""
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not api_key:
        raise ValueError("GROQ_API_KEY is required. Set it in .env file.")

    llm = ChatGroq(
        api_key=api_key,
        model=model,
        temperature=0.1,
        max_tokens=4096
    )
    return llm