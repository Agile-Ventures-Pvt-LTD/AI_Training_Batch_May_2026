import os
import shutil
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config
from embedding import embedder

def take_embeddings():
    return embedder()
    
def create_vector_db(chunks):
    """creating a new vector_db from the chunks"""
    if os.path.exists(Config.VECTOR_DB_DIR):
        shutil.rmtree(Config.VECTOR_DB_DIR)
    loader = Chroma.from_documents(
        documents=chunks,
        embedding=take_embeddings(),
        persist_directory=Config.VECTOR_DB_DIR
    )
    return loader

def load_vector_db():
    """load the sored vector_db for retrivel"""
    
    if not os.path.exists(Config.VECTOR_DB_DIR):
        return None
    
    result = Chroma(persist_directory=Config.VECTOR_DB_DIR, embedding_function=take_embeddings())
    return result