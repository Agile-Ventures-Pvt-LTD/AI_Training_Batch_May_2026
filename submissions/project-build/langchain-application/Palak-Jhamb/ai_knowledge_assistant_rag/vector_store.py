import time

# from chunking import split_documents
from chunking import split_documents
from config import DB_PATH
from embeddings import get_embedding_model
from loaders import load_documents
import chromadb
from langchain_chroma import Chroma

def create_vector_store(folder_path):
    documents = load_documents(folder_path)
    chunks= split_documents(documents)
    
    embedding_model = get_embedding_model()

    chromadb_client = chromadb.PersistentClient(path=DB_PATH)
    print("Database Created at:", DB_PATH)

    
    vectorstore = Chroma(
    collection_name="amazon_docs",
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding_model,
    client=chromadb_client,
    persist_directory=DB_PATH
    )
    print("Vector Store Created")
    print("Adding documents to the vector store")
    print(chromadb_client.count_collections())
    print("total chunks to add:", len(chunks))
    i = 0
    while i < len(chunks):
        vectorstore.add_documents( 
            documents=chunks[i:i+100], 
            ids=["text_" + str(i) for i in range(i, i+100)],
        )
    
        i += 100
        print(f"Added {i} / {len(chunks)} chunks to the vector store")
        time.sleep(1)

    return vectorstore
