import os, json
import config
from loaders import load_documents
from chunking import chunk_documents
from retrievers import get_vectorstore



def init_vectorstore():
    if os.path.exists(config.VECTOR_STORE_PATH) and os.listdir(config.VECTOR_STORE_PATH):
        print("Vector store ready.")
        return
    print("Creating vector store...")
    docs = load_policy_documents(config.KB_DATA_PATH)
    chunks = chunk_documents(docs, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    get_vectorstore(chunks)
    print("Vector store created.")

if __name__ == "__main__":
    init_vectorstore()
    while True:
        q = input("\nAsk query (or 'quit' to exit): ")
        if q.lower() == 'quit':
            break
        print((q))