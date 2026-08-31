from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import VECTOR_DB_PATH, EMBEDDING_MODEL


def create_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL,model_kwargs={"device": "cpu"})
    return embeddings


def build_vector_store(chunks, persist=True):
    embeddings = create_embeddings()
    vector_dir = Path(VECTOR_DB_PATH)
    vector_dir.mkdir(parents=True, exist_ok=True)
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(vector_dir),
        collection_name="it_troubleshooting"
    )
    return vector_store

def load_vector_store():
    vector_dir = Path(VECTOR_DB_PATH)
    if not vector_dir.exists():
        return None
    embeddings = create_embeddings()
    vector_store = Chroma(
        persist_directory=str(vector_dir),
        embedding_function=embeddings,
        collection_name="it_troubleshooting"
    )
    return vector_store


def get_or_create_vector_store(chunks=None):
    vector_store = load_vector_store()
    if vector_store is None and chunks:
        vector_store = build_vector_store(chunks)
    
    return vector_store
