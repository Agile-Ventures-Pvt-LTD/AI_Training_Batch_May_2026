import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm() -> ChatGroq:
    """
    Initialize and return the Groq LLM.
    """

    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=os.getenv("GROQ_MODEL"),
        temperature=0,
    )


