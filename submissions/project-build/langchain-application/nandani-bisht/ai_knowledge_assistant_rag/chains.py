from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from config import settings
from prompts import ANSWER_PROMPT


def build_chain():

    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_MODEL
    )

    chain = (
        ANSWER_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain