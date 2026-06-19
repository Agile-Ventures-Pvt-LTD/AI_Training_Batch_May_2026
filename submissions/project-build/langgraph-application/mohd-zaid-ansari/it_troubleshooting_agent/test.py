from config import KB_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from loaders import load_raw_documents
from chunking import process_and_chunk_documents
from embeddings import get_embedding_model
from vector_store import create_vectorstore, index_chunks_to_vectorstore
from retrievers import get_retriever, search_knowledge_base

def run_pipeline():
   
    raw_docs = load_raw_documents(KB_PATH)
    print(f"Loaded {len(raw_docs)} files.")

    final_chunks = process_and_chunk_documents(raw_docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    print(f"Created {len(final_chunks)} optimized chunks ready for embedding.")

    embedding_engine = get_embedding_model()
    print("HuggingFace embedding engine successfully initialized.")

    vector_db = create_vectorstore(embedding_engine)

    index_chunks_to_vectorstore(final_chunks, vector_db)
    retriever = get_retriever(vector_db)
    test_query = "How do I resolve ticket error 404?"  # Change to match your KB content
    print(f"\n🔍 Searching for: '{test_query}'...")
    
    results = search_knowledge_base(test_query, retriever)

    print(f"\nFound {len(results)} relevant matching chunks:\n")
    for i, doc in enumerate(results, start=1):
        print(f"--- Result #{i} ---")
        print(f"Source File: {doc.metadata.get('source')}")
        print(f"Section Path: Header 1 -> {doc.metadata.get('Header 1')}, Header 2 -> {doc.metadata.get('Header 2')}")
        print(f"Content Sneak Peek:\n{doc.page_content[:200]}...")
        print("-" * 20 + "\n")

if __name__ == "__main__":
    chunks = run_pipeline()


from tools import issue_classifiction, classify_and_retrieve, get_user_profile

user_query = "Who is user USR-1001"


info=get_user_profile(user_id=1001)
print(info)

from db_utils import execute_query

from tools import get_user_profile, get_device_status, get_incident_details, run_diagnostic_check, get_ticket_details
from prebuilt_agent import prebuilt_agent

result = get_user_profile("USR-1001")
print(result)

result=get_device_status("USR-1001")
print(result)

result=get_incident_details("INC-4001")
print(result)

result=run_diagnostic_check("USR-1001")
print(result)

result=get_ticket_details("IT-3001")
print(result)

result=prebuilt_agent(" Amit VPN Timeout")
print(result)








