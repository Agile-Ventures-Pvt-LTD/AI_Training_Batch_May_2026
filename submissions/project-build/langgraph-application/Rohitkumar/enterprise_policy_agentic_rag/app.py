import os, json
import config
from loaders import load_policy_documents
from chunking import chunk_documents
from retrievers import get_vectorstore
from graph import run_policy_assistant

def init_vectorstore():
    if os.path.exists(config.VECTOR_STORE_PATH) and os.listdir(config.VECTOR_STORE_PATH):
        print("Vector store ready.")
        return
    print("Creating vector store...")
    docs = load_policy_documents(config.POLICY_DATA_PATH)
    chunks = chunk_documents(docs, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    get_vectorstore(chunks)
    print("Vector store created.")

def ask_question(question):
    return run_policy_assistant(question)

if __name__ == "__main__":
    init_vectorstore()
    while True:
        q = input("\nAsk a policy question (or 'quit' to exit): ")
        if q.lower() == 'quit':
            break
        print(ask_question(q))