
import os
import chromadb
from langchain_chroma import Chroma
from embeddings import embedding_model

persist_directory = "./data/vector_store"
chunk_collection_name = "amazon-chunks"

chromadb_client = chromadb.PersistentClient(path=persist_directory)

vector_db = Chroma(
    collection_name=chunk_collection_name,
    collection_metadata={"hnsw:space": "cosine"}, 
    embedding_function=embedding_model,
    client=chromadb_client, 
    persist_directory=persist_directory
)
