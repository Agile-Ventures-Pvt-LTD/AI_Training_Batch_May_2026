import chromadb

from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def get_vector_db():
    client = chromadb.PersistentClient(
        path="data/vector_store"
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma(
        client=client,
        embedding_function=embeddings
    )


def get_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={"k": 3}
    )


def email_outlook_troubleshooing_guide_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"issue_domain": "email_outlook_troubleshooting_guide"}
        }
    )


def laptop_performance_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"issue_domain": "laptop_performance_guide"}
        }
    )


def network_connectivity_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"issue_domain": "network_connectivity_guide"}
        }
    )


def password_reset_guide_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"issue_domain": "password_reset_guide"}
        }
    )


def printer_troubleshooting_guide_retriever():

    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"issue_domain": "printer_troubleshooting_guide"}
        }
    )


