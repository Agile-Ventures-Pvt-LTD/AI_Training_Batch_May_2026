from crewai import LLM
from config import GROQ_API_KEY, GROQ_MODEL

_default_llm = LLM(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0
)