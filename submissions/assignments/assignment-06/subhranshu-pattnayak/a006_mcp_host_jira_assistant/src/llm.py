from langchain_groq import ChatGroq
try:
    from src_config import GROQ_API_KEY, GROQ_MODEL
except ImportError:
    from .src_config import GROQ_API_KEY, GROQ_MODEL


default_llm = ChatGroq(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0
)