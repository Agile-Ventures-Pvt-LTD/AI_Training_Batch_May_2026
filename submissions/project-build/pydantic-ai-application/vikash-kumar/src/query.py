import chromadb
from chromadb.utils import embedding_functions

def query_knowledge_base(user_question: str, db_dir: str = "./ecommerce_bot_db", num_results: int = 3):
    """Searches the persistent disk index to fetch highly relevant contextual information."""
    # Mount the local database folder structure
    client = chromadb.PersistentClient(path=db_dir)
    
    # Utilize the same localized mathematical embedding pipeline
    local_embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    try:
        # Retrieve the collection matching the ingested name
        collection = client.get_collection(
            name="ebay_seller_policies", 
            embedding_function=local_embedder
        )
    except Exception:
        print(f"Error: Collection not found. Please execute 'ingest.py' first to build '{db_dir}'.")
        return

    # Query matching matrices
    results = collection.query(
        query_texts=[user_question],
        n_results=num_results
    )
    
    # Display the matched records clean
    print(f"\n--- Top {num_results} Matches for: '{user_question}' ---")
    
    zipped_results = zip(results['documents'][0], results['metadatas'][0], results['distances'][0])
    for idx, (doc, meta, dist) in enumerate(zipped_results, start=1):
        print(f"\n[Result #{idx}] (Confidence Vector Distance: {dist:.4f})")
        print(f"Location: Page {meta['page_number']} in {meta['source_file']}")
        print(f"Content snippet: {doc.strip()}")
        print("-" * 40)

if __name__ == "__main__":
    # Test queries directly mirroring information present inside your vendor manual
    test_query = "What are the rules and requirements to achieve PowerSeller status?"
    query_knowledge_base(user_question=test_query)
