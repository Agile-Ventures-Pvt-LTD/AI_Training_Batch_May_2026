# rag.py 
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter


# rag.py

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "logistics_rules"


client = chromadb.PersistentClient(path=CHROMA_DB_PATH)


def create_vector_db():
    collection_names = [c.name for c in client.list_collections()]

    if COLLECTION_NAME in collection_names:
        return

    text_path = Path("data") / "logistics_knowledge_base.txt"

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=30)
    chunks = splitter.split_text(text)
    
    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction()
    )

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks
    )


def retrieve_rules(query: str, k: int = 3) -> str:
    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction()
    )

    result = collection.query(query_texts=[query], n_results=k)
    docs = result["documents"][0]

    return "\n\n".join(docs)

