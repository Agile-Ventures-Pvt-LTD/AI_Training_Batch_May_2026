
# src/rag.py
import json
from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

KB_PATH = Path(__file__).parents[1] / "data" / "logistics_knowledge_base.txt"

_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
_vectorstore: FAISS | None = None


def _load_vectorstore() -> FAISS:
    global _vectorstore
    if _vectorstore is None:
        if not KB_PATH.is_file():
            raise FileNotFoundError(f"Knowledge base not found at {KB_PATH}")

        text = KB_PATH.read_text(encoding="utf-8")
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.create_documents([text])
        _vectorstore = FAISS.from_documents(docs, _embeddings)
    return _vectorstore


def retrieve_rules(query: str, k: int = 3) -> str:
    store = _load_vectorstore()
    docs = store.similarity_search(query, k=k)
    # Join with a newline for readability
    return "\n".join(d.page_content for d in docs)
