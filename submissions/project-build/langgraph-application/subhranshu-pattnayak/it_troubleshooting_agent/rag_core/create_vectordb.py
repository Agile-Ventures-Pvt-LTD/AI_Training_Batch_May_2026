from utils.paths import vector_path, raw_data_path, collection_name
from rag_core.loader import load_files
from rag_core.chunker import chunk_documents
from rag_core.embedding import init_embedding
from langchain_chroma import Chroma
import chromadb
import os


def create_db():
    try:
        docs = load_files(raw_data_path)
        print(f"Documents Loaded: {len(docs)}")
        chunks = chunk_documents(docs)
        print(f"Total Chunks: {len(chunks)}")
        embedding_model = init_embedding()
        chromadb_client = chromadb.PersistentClient(path=vector_path)
        vectorstore = Chroma.from_documents(
            chunks,
            embedding_model,
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"},
            persist_directory=vector_path,
            client=chromadb_client
        )
        return chromadb_client, vectorstore
    except Exception as e:
        print(f"Error: {e}")