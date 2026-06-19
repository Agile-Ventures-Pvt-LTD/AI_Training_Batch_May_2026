import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from config import EMBEDDING_MODEL, VECTOR_STORE_PATH, TOP_K
from loaders import load_and_chunk_knowledge_base


ISSUE_DOMAIN_KEYWORDS = {
    "VPN": ["vpn", "virtual private network", "tunnel", "gateway", "vpn timeout", "vpn disconnect"],
    "OUTLOOK_EMAIL": ["outlook", "email", "mail", "exchange", "sync", "mailbox", "outbox", "inbox"],
    "LAPTOP_PERFORMANCE": ["laptop", "slow", "performance", "cpu", "memory", "disk", "startup", "boot"],
    "PASSWORD_RESET": ["password", "login", "account", "locked", "reset", "mfa", "authentication", "access"],
    "NETWORK_CONNECTIVITY": ["network", "internet", "connectivity", "wifi", "wi-fi", "connection", "dns"],
    "PRINTER": ["printer", "print", "printing", "queue", "offline printer"],
}


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vector_store(chunks=None, persist_directory=None):
    if persist_directory is None:
        persist_directory = os.path.abspath(VECTOR_STORE_PATH)

    os.makedirs(persist_directory, exist_ok=True)

    if chunks is None:
        chunks = load_and_chunk_knowledge_base()

    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="it_troubleshooting_kb",
    )

    print(f"Vector store built with {len(chunks)} chunks and persisted to {persist_directory}")
    return vector_store


def load_vector_store(persist_directory=None):
    if persist_directory is None:
        persist_directory = os.path.abspath(VECTOR_STORE_PATH)

    embeddings = get_embeddings()

    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name="it_troubleshooting_kb",
        )
        return vector_store
    else:
        return build_vector_store(persist_directory=persist_directory)


def get_retriever(vector_store=None, top_k=None):
    if top_k is None:
        top_k = TOP_K

    if vector_store is None:
        vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )
    return retriever


def retrieve_by_issue_type(issue_type, query, vector_store=None, top_k=None):
    if top_k is None:
        top_k = TOP_K

    if vector_store is None:
        vector_store = load_vector_store()

    domain_filter = {"issue_domain": issue_type}

    try:
        results = vector_store.similarity_search(
            query,
            k=top_k,
            filter=domain_filter,
        )
        if not results:
            results = vector_store.similarity_search(query, k=top_k)
    except Exception:
        results = vector_store.similarity_search(query, k=top_k)

    return results


def format_retrieved_chunks(documents):
    chunks = []
    for doc in documents:
        chunks.append({
            "source_file": doc.metadata.get("source_file", "unknown"),
            "chunk_id": doc.metadata.get("chunk_id", ""),
            "issue_domain": doc.metadata.get("issue_domain", "GENERAL"),
            "snippet": doc.page_content[:500],
        })
    return chunks
