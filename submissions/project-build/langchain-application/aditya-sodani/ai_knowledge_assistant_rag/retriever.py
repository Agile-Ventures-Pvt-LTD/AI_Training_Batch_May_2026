from langchain_chroma import Chroma
from config import Config
from embeddings import get_embedding_model

def get_retriever():
    
    embeddings = get_embedding_model()
    vector_store = Chroma(
        persist_directory=str(Config.VECTOR_STORE_DIR), 
        embedding_function=embeddings
    )
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})