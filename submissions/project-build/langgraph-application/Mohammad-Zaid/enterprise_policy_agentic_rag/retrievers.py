# file: retrievers.py

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from loaders import load_documents
from chunking import split_and_set_metadata
from config import EMBEDDING_MODEL, VECTOR_STORE_PATH


def get_vector_db():

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_db = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embedding_model
    )

    if vector_db._collection.count() == 0:

        docs = load_documents()
        chunks = split_and_set_metadata(docs)

        vector_db.add_documents(
            documents=chunks,
            ids=[
                chunk.metadata["chunk_id"]
                for chunk in chunks
            ]
        )

    return vector_db


def search_policy(query, policy_name, k=4):

    vector_db = get_vector_db()

    docs = vector_db.similarity_search(
        query=query,
        k=k
    )

    filtered_docs = []

    for doc in docs:
        if policy_name in doc.metadata.get(
            "policy_domain", ""
        ):
            filtered_docs.append(doc)

    return filtered_docs