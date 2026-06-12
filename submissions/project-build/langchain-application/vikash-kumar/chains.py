from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from config import GROQ_MODEL

from prompts import (CLASSIFICATION_PROMPT,RAG_PROMPT)

llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0
)


def classify_query(query):

    prompt = ChatPromptTemplate.from_template(CLASSIFICATION_PROMPT)

    chain = prompt | llm

    response = chain.invoke(
        {
            "query": str(query)
        }
    )

    return response


def generate_answer(question,docs):
    context = "\n\n".join(
        [doc.page_content for doc in docs])

    prompt = ChatPromptTemplate.from_template(RAG_PROMPT)

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": str(question),
            "context": str(context)
        })

    return response