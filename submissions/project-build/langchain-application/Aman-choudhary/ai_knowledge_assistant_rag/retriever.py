from langchain_chroma import Chroma
from config import Config
from embeddings import get_embedding_model

def get_retriever():
    """
    Initializes and returns a retriever from the persisted vector store.
    """
    embeddings = get_embedding_model()
    vector_store = Chroma(
        persist_directory=str(Config.VECTOR_STORE_DIR), 
        embedding_function=embeddings
    )
    # We retrieve the top 4 most relevant chunks for context
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})