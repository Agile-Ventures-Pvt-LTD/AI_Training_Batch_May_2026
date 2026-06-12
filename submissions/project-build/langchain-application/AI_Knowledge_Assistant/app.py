import os
import traceback
from dotenv import load_dotenv
from doc_loader import load_documents
from chunker import chunk_documents
from vector_store import get_vector_store
from retriever import get_retriever
from chains import respond, print_result

load_dotenv()

if __name__ == "__main__":
    print("[1] starting")
    vector_store_path = os.environ.get("VECTOR_STORE_DIR", "data/vector_store")
    print(f"[2] vector store path: {vector_store_path}")
    print(f"[3] exists: {os.path.exists(vector_store_path)}")

    if os.path.exists(vector_store_path):
        print("[4] loading...")
        db = get_vector_store()
    else:
        print("[4] building...")
        docs = load_documents()
        print("[5] docs loaded")
        chunks = chunk_documents(docs)
        print(f"[6] chunks created: {len(chunks)}")
        print(f"[6b] sample chunk: {chunks[0].page_content[:100]}")
        print(f"[6c] sample metadata: {chunks[0].metadata}")
        chunks = chunks[:50]

        try:
            db = get_vector_store(chunks)
            print(f"[7] db: {db}")

        except Exception as e:
            traceback.print_exc()
            exit()

        if db is None:
            print("[ERROR] Vector store is None, exiting.")
            exit()

    print("[8] getting retriever...")
    retriever = get_retriever(db)
    print("[9] retriever ready, starting chat...")

    while True:
        question = input("\nUser (type q to quit): ")
        if question == "q":
            break
        result = respond(question, retriever)
        print_result(result)