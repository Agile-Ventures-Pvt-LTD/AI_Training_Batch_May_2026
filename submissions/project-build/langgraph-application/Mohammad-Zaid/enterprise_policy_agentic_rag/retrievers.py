import chromadb
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTOR_STORE_PATH = "./vector_store"
COLLECTION_NAME = "policy-chunks"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SEARCH_K = 3

def initialize_vector_store(chunks):
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    chromadb_client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
    vector_db = Chroma(
        collection_name=COLLECTION_NAME,
        collection_metadata={"hnsw:space": "cosine"},
        embedding_function=embedding_function,
        client=chromadb_client,
        persist_directory=VECTOR_STORE_PATH,
    )
    if chunks:
        vector_db.add_documents(
            documents=chunks,
            ids=[chunk.metadata.get("chunk_id") for chunk in chunks],
        )
    return vector_db
    
    return vector_db


def get_retriever(vector_db):
    """
    Create a retriever from the vector store.
    
    Args:
        vector_db (Chroma): Initialized vector store
        
    Returns:
        Retriever: Configured retriever for similarity search
    """
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": SEARCH_K},
    )
    
    return retriever
