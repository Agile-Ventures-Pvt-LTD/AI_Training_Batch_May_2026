import os

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import VECTOR_DB_PATH
from embeddings import get_embedding_model


def create_documents(chunk_data):
    
    # Convert chunk json into LangChain Documents.
    
    docs = []

    for chunk in chunk_data:
        docs.append(
            Document(
                page_content=chunk["text"],
                metadata=chunk["metadata"]
            )
        )
    return docs


def build_vector_store(chunk_data):

    embeddings = get_embedding_model()

    documents = create_documents(chunk_data)

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    print(
        f"Vector store created with "
        f"{len(documents)} chunks."
    )

    return vector_store


def load_vector_store():

    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError(
            "Vector database not found."
        )

    embeddings = get_embedding_model()

    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return vector_store