from vectorstore import get_vector_store
from config import TOP_K


def _format_results(results) -> list[dict]:
    formatted = []
    for doc, score in results:
        formatted.append({
            "policy_domain": doc.metadata.get("policy_domain", "OTHER"),
            "source_file": doc.metadata.get("source_file", ""),
            "chunk_id": doc.metadata.get("chunk_id", ""),
            "content": doc.page_content,
            "relevance_score": round(max(0.0, 1.0 - score), 4),
        })
    return formatted

def retrieve_by_domain(query: str, policy_domain: str, top_k: int = None) -> list[dict]:
    db = get_vector_store()
    results = db.similarity_search_with_score(
        query, k=TOP_K, filter={"policy_domain": policy_domain}
    )
    return _format_results(results)
