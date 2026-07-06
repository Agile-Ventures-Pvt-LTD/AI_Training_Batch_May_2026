"""Vector Store Creation pipeline.

To be used when persistent database is not available or provided.
"""

import os
import chromadb
import warnings
from typing import Any
from utils.loader import load_file
from langchain_chroma import Chroma
try:
    from utils.chunker import chunk_documents
    from utils.embedding import init_embedding
    from utils.config import COLLECTION_NAME, DB_PATH, file_path
except ImportError:
    from .utils.chunker import chunk_documents
    from .utils.embedding import init_embedding
    from .utils.config import COLLECTION_NAME, DB_PATH, file_path


warnings.filterwarnings("ignore")

def createVectorStore():
    """Create the vector store for the given data.
    """
    if not os.path.exists(os.path.dirname(file_path)):
        raise Exception(f"[ERROR] Directory ({os.path.dirname(file_path)}) not found")
    
    # Loading the file into documents
    docs = load_file(file_path=file_path)
    if not docs:
        raise Exception(f"[ERROR] No content loaded for {os.path.basename(file_path)}")
    print(f"FILES LOADED SUCCESSFULLY: {len(docs)}")
    
    #Chunking the documents into chunks of size 800 with 150 overlap maintaining an 18% overlap for optimal performance, subject to change.
    chunks = chunk_documents(docs)
    c_id = 0
    for chunk in chunks:
        chunk.metadata["chunk_id"] = "text_"+str(c_id)
        chunk.id = "text_"+str(c_id)
        c_id += 1
    if not chunks:
        raise Exception(f"[ERROR] No chunks created.")
    print(f"DOCUMENTS CHUNKED SUCCESSFULLY: {len(chunks)}")
    
    # Embedding the chunks using all-mpnet-base-v2 embedding model from HuggingFace.
    embedding_model = init_embedding()
    
    # Initializing chromadb persistent client
    chromadb_client = chromadb.PersistentClient(path=DB_PATH)
    print("CHROMADB PERSISTENT CLIENT INITIALIZED.")
    
    # Creating a persistent vector store from chunks using embeddings and persistent client.
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=DB_PATH,
        client=chromadb_client
    )
    print("VECTORSTORE INITIALIZED FROM CHUNKS.")
    
    # Logging and error handling.
    heartbeat = chromadb_client.heartbeat() 
    collections = chromadb_client.count_collections()
    records = chromadb_client.get_collection(COLLECTION_NAME).count()
    if not heartbeat or not collections or not records:
        raise Exception(f"[ERROR] FAILED TO CREATE THE VECTOR STORE.\nChromaDB HEARTBEAT: {heartbeat}\COLLECTIONS: {collections}\TOTAL RECORDS: {records}")
    
    message = f"VECTOR STORE SUCCESSFULLY CREATED.\nCOLLECTIONS: {collections}\nTOTAL RECORDS: {records}"
    return message, vectorstore






def retrieve(query: str) -> list[Any]:
    """Retrieve chunks from Vector Database

    Args:
        query (str): Input query

    Returns:
        List[Any]: List of document chunks
    """
    
    vectorstore_persisted = Chroma(
        collection_name=COLLECTION_NAME,
        collection_metadata={"hnsw:space": "cosine"},
        embedding_function=init_embedding(),
        persist_directory=DB_PATH
    )

    retriever = vectorstore_persisted.as_retriever(
        search_type="similarity",
        search_kwargs={
            'k': 3
        }
    )
    
    return retriever.invoke(query)

if __name__ == "__main__":
    message, vectorstore = createVectorStore()
    print(type(vectorstore))
    print(message)