import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL,VECTOR_STORE_DIR

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def get_vector_store(chunks: list = None) -> Chroma:
    embedding_model = get_embedding_model()
    
    if Path(VECTOR_STORE_DIR).exists() and chunks is None:
        print("[INFO] Loading existing vector store...")
        return Chroma(
            persist_directory=VECTOR_STORE_DIR,
            embedding_function=embedding_model,
            collection_name="knowledge_base",
        )
    
    print("[INFO] Building vector store...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=VECTOR_STORE_DIR,
        collection_name="knowledge_base",
    )
    print(f"[INFO] Done. Collection count: {db._collection.count()}")
    return db