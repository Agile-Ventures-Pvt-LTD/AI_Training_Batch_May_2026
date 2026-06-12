from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from config import Config
from prompts import get_classification_prompt, get_grounded_answer_prompt

def get_classification_chain():
    """
    Chain for classifying queries before retrieval.
    """
    llm = ChatGroq(
        groq_api_key=Config.GROQ_API_KEY,
        model_name=Config.GROQ_MODEL_NAME,
        temperature=0
    )
    return get_classification_prompt() | llm | JsonOutputParser()

def get_grounded_rag_chain():
    """
    Chain for generating answers strictly from context.
    """
    llm = ChatGroq(
        groq_api_key=Config.GROQ_API_KEY,
        model_name=Config.GROQ_MODEL_NAME,
        temperature=Config.TEMPERATURE
    )
    return get_grounded_answer_prompt() | llm | JsonOutputParser()