import os

from langchain_chroma import Chroma

from config import VECTOR_DB_PATH

from embeddings import get_embedding_model

def create_vector_store(chunks):
    embeddings =  get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding= embeddings,
        persist_directory= VECTOR_DB_PATH
    )

    return vector_store

def load_vector_store():
    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError("Vector Store not FOund")
    
    embeddings = get_embedding_model()

    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

