from langchain_groq import ChatGroq

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

from prompts import (
    QUERY_CLASSIFICATION_PROMPT,
    RAG_PROMPT
)

from output_parser import (
    parse_json_response
)


def get_llm():

    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0
    )


def classify_query(
    question
):

    llm = get_llm()

    chain = (
        QUERY_CLASSIFICATION_PROMPT
        | llm
    )

    response = chain.invoke(
        {
            "question": question
        }
    )

    return parse_json_response(
        response.content
    )


def generate_answer(
    question,
    context
):

    llm = get_llm()

    chain = (
        RAG_PROMPT
        | llm
    )

    response = chain.invoke(
        {
            "question": question,
            "context": context
        }
    )

    return parse_json_response(
        response.content
    )