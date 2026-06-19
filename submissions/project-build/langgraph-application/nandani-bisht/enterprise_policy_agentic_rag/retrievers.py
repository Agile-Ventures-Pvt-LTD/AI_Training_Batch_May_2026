import logging
from pathlib import Path
from typing import List, Dict
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import config

logger = logging.getLogger(__name__)

_vectorstore: Chroma | None = None
_embeddings: HuggingFaceEmbeddings | None = None


def get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings


def build_vectorstore(chunks: List[Document]) -> Chroma:
    global _vectorstore
    embeddings = get_embeddings()
    _vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.VECTOR_STORE_PATH,
        collection_name="policy_documents",
    )
    logger.info("Vector store built with %d chunks", len(chunks))
    return _vectorstore


def load_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    store_path = Path(config.VECTOR_STORE_PATH)
    embeddings = get_embeddings()
    _vectorstore = Chroma(
        persist_directory=str(store_path),
        embedding_function=embeddings,
        collection_name="policy_documents",
    )
    logger.info("Vector store loaded from disk")
    return _vectorstore


def retrieve_by_domain(query: str, domain: str, top_k: int = None) -> List[Dict]:
    k = top_k or config.TOP_K
    store = load_vectorstore()

    results = store.similarity_search_with_relevance_scores(
        query,
        k=k * 2,
        filter={"policy_domain": domain},
    )

    chunks = []
    for doc, score in results[:k]:
        chunks.append(
            {
                "policy_domain": doc.metadata.get("policy_domain", domain),
                "source_file": doc.metadata.get("source_file", ""),
                "chunk_id": doc.metadata.get("chunk_id", ""),
                "content": doc.page_content,
                "relevance_score": round(float(score), 4),
            }
        )

    return chunks


def retrieve_across_domains(query: str, domains: List[str], top_k: int = None) -> List[Dict]:
    all_chunks = []
    for domain in domains:
        chunks = retrieve_by_domain(query, domain, top_k)
        all_chunks.extend(chunks)

    all_chunks.sort(key=lambda x: x["relevance_score"], reverse=True)
    return all_chunks
