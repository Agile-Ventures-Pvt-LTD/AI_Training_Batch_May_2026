from langchain_chroma import Chroma
from config import Config
from embeddings import get_embedding_model

def create_vector_store(chunks):
    """
    Creates a Chroma vector store from document chunks and persists it to disk.
    """
    embeddings = get_embedding_model()
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(Config.VECTOR_STORE_DIR)
    )
    
    print(f"Vector store successfully created at: {Config.VECTOR_STORE_DIR}")
    return vector_store