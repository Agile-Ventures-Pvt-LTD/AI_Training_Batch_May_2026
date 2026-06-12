from vector_store import load_vector_store
from config import settings


def get_retriever():

    db = load_vector_store()

    return db.as_retriever(
        search_kwargs={
            "k": settings.TOP_K
        }
    )


def retrieve_documents(question):

    retriever = get_retriever()

    return retriever.invoke(
        question
    )