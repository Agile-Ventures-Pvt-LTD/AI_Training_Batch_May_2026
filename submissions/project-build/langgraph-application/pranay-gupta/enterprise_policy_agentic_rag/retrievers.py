from vector_store import load_vector_db, search_documents
from config import TOP_K

def retrieve(query, k=TOP_K):
    """
    Retrieve top k relevant policy chunks.
    
    Returns:
        List of chunks with structure:
        {
            "policy_domain": "TRAVEL",
            "source_file": "travel_policy.md",
            "chunk_id": "chunk_001",
            "content": "Policy text...",
            "relevance_score": 0.85
        }
    """
    db = load_vector_db()
    results = search_documents(db, query, k=k)
    
    chunks = []
    for doc, score in results:
        chunk = {
            "policy_domain": doc.metadata.get("policy_domain", "UNKNOWN"),
            "source_file": doc.metadata.get("source_file", ""),
            "chunk_id": doc.metadata.get("chunk_id", ""),
            "content": doc.page_content,
            "relevance_score": float(score)
        }
        chunks.append(chunk)
    
    return chunks
