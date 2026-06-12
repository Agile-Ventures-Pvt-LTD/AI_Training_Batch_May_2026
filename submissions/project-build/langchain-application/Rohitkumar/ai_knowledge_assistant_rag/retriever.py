from typing import Any, Dict, List, Optional

from config import EMBEDDING_MODEL_NAME, TOP_K
from embeddings import EmbeddingModel
from vector_store import create_vector_store, InMemoryVectorStore, ChromaVectorStore


def build_retriever(
    chunks: List[Dict[str, Any]],
    embeddings: List[List[float]],
    embedding_model: Optional[EmbeddingModel] = None,
) -> Any:
    """Build a vector store retriever from chunks and their embeddings."""
    return create_vector_store(chunks, embeddings)


def retrieve(
    question: str,
    vector_store: Any,
    embedding_model: EmbeddingModel,
    top_k: int = TOP_K,
) -> List[Dict[str, Any]]:
    """Embed the question and retrieve top-k similar chunks from the vector store."""
    query_embedding = embedding_model.embed_query(question)
    return vector_store.similarity_search(query_embedding, top_k=top_k)


def format_retrieved_chunks(retrieved_chunks: List[Dict[str, Any]]) -> str:
    """Format retrieved chunks into a human-readable debug string."""
    lines = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        score = chunk.get("similarity_score", "N/A")
        if isinstance(score, float):
            score = f"{score:.4f}"
        lines.append(
            f"Rank {i} | Score: {score}\n"
            f"  Source: {chunk['source_file']} | Page: {chunk['page_number']} | Chunk: {chunk['chunk_id']}\n"
            f"  Preview: {chunk['text'][:200]}...\n"
        )
    return "\n".join(lines)