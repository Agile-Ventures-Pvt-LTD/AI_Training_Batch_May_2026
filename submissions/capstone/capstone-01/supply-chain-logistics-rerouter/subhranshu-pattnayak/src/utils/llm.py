from langchain_groq import ChatGroq
try:
    from config import GROQ_API_KEY, GROQ_MODEL
except ImportError:
    from .config import GROQ_API_KEY, GROQ_MODEL

def get_client():
    return ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0
    )