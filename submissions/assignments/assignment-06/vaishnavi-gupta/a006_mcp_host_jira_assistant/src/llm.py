from langchain_groq import ChatGroq

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
)


class GroqLLM:
    """
    Wrapper class for initializing the Groq LLM.
    """

    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=0,
        )

    def get_llm(self):
        """
        Return the initialized ChatGroq instance.
        """
        return self.llm


# Singleton instance used throughout the project
groq_llm = GroqLLM().get_llm()