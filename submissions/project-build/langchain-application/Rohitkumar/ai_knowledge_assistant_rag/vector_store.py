import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import VECTOR_STORE_DIR

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

try:
    import numpy as np
except ImportError:
    np = None


def _ensure_vector_store_dir() -> None:
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)


class InMemoryVectorStore:
    def __init__(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        if np is None:
            raise ImportError("numpy is required for in-memory vector search fallback.")
        self.documents = []
        for chunk, vector in zip(chunks, embeddings):
            self.documents.append({**chunk, "embedding": np.array(vector, dtype=float)})

    def similarity_search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        query_vector = np.array(query_embedding, dtype=float)
        scores = []
        for doc in self.documents:
            embedding = doc["embedding"]
            norm = np.linalg.norm(embedding) * np.linalg.norm(query_vector)
            similarity = float(np.dot(embedding, query_vector) / norm) if norm > 0 else 0.0
            scores.append((similarity, doc))

        scores.sort(key=lambda item: item[0], reverse=True)
        result = []
        for similarity, doc in scores[:top_k]:
            doc_copy = {k: v for k, v in doc.items() if k != "embedding"}
            doc_copy["similarity_score"] = similarity
            result.append(doc_copy)
        return result


class ChromaVectorStore:
    COLLECTION_NAME = "rag_chunks"

    def __init__(self):
        if chromadb is None:
            raise ImportError("chromadb is required for persistent vector store. Install chromadb or update dependencies.")
        _ensure_vector_store_dir()
        self.client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
        self.collection = self.client.get_or_create_collection(name=self.COLLECTION_NAME)

    def add_documents(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        ids = [chunk["chunk_id"] for chunk in chunks]
        metadatas = [
            {
                "source_file": chunk["source_file"],
                "page_number": chunk["page_number"],
                "section_title": chunk.get("section_title", ""),
                "chunk_id": chunk["chunk_id"],
            }
            for chunk in chunks
        ]
        documents = [chunk["text"] for chunk in chunks]
        self.collection.add(
            ids=ids,
            metadatas=metadatas,
            documents=documents,
            embeddings=embeddings,
        )

    def similarity_search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k, include=['metadatas','documents','distances'])
        retrieved: List[Dict[str, Any]] = []
        for i, doc_id in enumerate(results["ids"][0]):
            retrieved.append(
                {
                    "chunk_id": doc_id,
                    "source_file": results["metadatas"][0][i].get("source_file", ""),
                    "page_number": results["metadatas"][0][i].get("page_number", ""),
                    "section_title": results["metadatas"][0][i].get("section_title", ""),
                    "text": results["documents"][0][i],
                    "similarity_score": float(results["distances"][0][i]) if results["distances"][0][i] is not None else 0.0,
                }
            )
        return retrieved


def create_vector_store(chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> Any:
    if chromadb is not None:
        store = ChromaVectorStore()
        store.add_documents(chunks, embeddings)
        return store
    return InMemoryVectorStore(chunks, embeddings)


def load_vector_store() -> Optional[Any]:
    if chromadb is None:
        return None
    try:
        store = ChromaVectorStore()
        return store
    except Exception:
        return None
