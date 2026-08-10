"""Vector Store Creation pipeline.

To be used when persistent database is not available or provided.
"""

import os
import chromadb
import warnings
from rag.loader import load_file
from langchain_chroma import Chroma
from rag.chunker import chunk_documents
from rag.embedding import init_embedding
from config import DATA_DIR, COLLECTION_NAME, DB_PATH

data_file_name = "Advanced_Business_Seller_Guide_May09.pdf"

warnings.filterwarnings("ignore")

def createVectorStore():
    if not os.path.exists(DATA_DIR):
        raise Exception(f"[ERROR] Directory ({DATA_DIR}) not found")
    
    # Configure the data file path
    file_path = os.path.join(DATA_DIR, data_file_name)
    
    # Loading the file into documents
    docs = load_file(file_path=file_path)
    if not docs:
        raise Exception(f"[ERROR] No content loaded for {data_file_name}")
    print("FILES LOADED SUCCESSFULLY")
    
    #Chunking the documents into chunks of size 800 with 150 overlap maintaining an 18% overlap for optimal performance, subject to change.
    chunks = chunk_documents(docs)
    c_id = 0
    for chunk in chunks:
        chunk.metadata["chunk_id"] = "text_"+str(c_id)
        c_id += 1
    if not chunks:
        raise Exception(f"[ERROR] No chunks created.")
    print("DOCUMENTS CHUNKED SUCCESSFULLY")
    
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

if __name__ == "__main__":
    message, vectorstore = createVectorStore()
    print(type(vectorstore))
    print(message)