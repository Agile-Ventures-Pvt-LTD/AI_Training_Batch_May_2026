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


def get_ai_usage_policy_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"policy_domain": "ai_usage_policy"}
        }
    )


def get_hr_leave_policy_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"policy_domain": "hr_leave_policy"}
        }
    )


def get_it_security_policy_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"policy_domain": "it_security_policy"}
        }
    )


def get_reimbursement_policy_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"policy_domain": "reimbursement_policy"}
        }
    )


def get_travel_policy_retriever():
    db = get_vector_db()

    return db.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"policy_domain": "travel_policy"}
        }
    )


def docs_to_text(docs):
    text = ""

    for doc in docs:
        source = doc.metadata.get("source_file", "unknown")
        text += f"Source: {source}\n"
        text += doc.page_content
        text += "\n\n"

    return text.strip()


def run_retriever(query, retriever):
    docs = retriever.invoke(query)

    if not docs:
        return "No matching policy content found."

    return docs_to_text(docs)


@tool
def retrieve_ai_usage_policy(query: str) -> str:
    """Retrieve relevant chunks only from ai_usage_policy.md."""
    retriever = get_ai_usage_policy_retriever()
    return run_retriever(query, retriever)


@tool
def retrieve_hr_leave_policy(query: str) -> str:
    """Retrieve relevant chunks only from hr_leave_policy.md."""
    retriever = get_hr_leave_policy_retriever()
    return run_retriever(query, retriever)


@tool
def retrieve_it_security_policy(query: str) -> str:
    """Retrieve relevant chunks only from it_security_policy.md."""
    retriever = get_it_security_policy_retriever()
    return run_retriever(query, retriever)


@tool
def retrieve_reimbursement_policy(query: str) -> str:
    """Retrieve relevant chunks only from reimbursement_policy.md."""
    retriever = get_reimbursement_policy_retriever()
    return run_retriever(query, retriever)


@tool
def retrieve_travel_policy(query: str) -> str:
    """Retrieve relevant chunks only from travel_policy.md."""
    retriever = get_travel_policy_retriever()
    return run_retriever(query, retriever)


POLICY_RETRIEVER_TOOLS = [
    retrieve_ai_usage_policy,
    retrieve_hr_leave_policy,
    retrieve_it_security_policy,
    retrieve_reimbursement_policy,
    retrieve_travel_policy,
]

POLICY_RETRIEVER_TOOL_BY_DOMAIN = {
    "ai_usage_policy": retrieve_ai_usage_policy,
    "hr_leave_policy": retrieve_hr_leave_policy,
    "it_security_policy": retrieve_it_security_policy,
    "reimbursement_policy": retrieve_reimbursement_policy,
    "travel_policy": retrieve_travel_policy,
}
