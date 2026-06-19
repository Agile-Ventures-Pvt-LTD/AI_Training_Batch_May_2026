from config import TOP_K
from typing import Dict, Any, List

class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve_troubles_chunks(self, query: str, issue_domain: str, top_k: int = TOP_K) -> List[Dict[str, Any]]:
        print(f"-> [Retriever] Fetching from domain '{issue_domain}' for query: '{query}'")
        results = self.vector_store.similarity_search_with_relevance_scores(query=query,k=top_k,filter={"issue_domain": issue_domain})
        
        retrieved_chunks = []
        for doc, score in results:
            retrieved_chunks.append({
                "issue_domain": doc.metadata.get("issue_domain"),
                "source_file": doc.metadata.get("source_file"),
                "chunk_id": doc.metadata.get("chunk_id"),
                "snippet": doc.page_content,
                "relevance_score": round(float(score), 2)
            })

        return retrieved_chunks

    def retrieve_troubleshooting_steps(self, issue_type: str, query: str, top_k: int = TOP_K) -> Dict[str, Any]:
        domain = issue_type.lower()
        chunks = self.retrieve_troubles_chunks(query=query, issue_domain=domain, top_k=top_k)
        
        cleaned_chunks = [
            {
                "source_file": c["source_file"],
                "chunk_id": c["chunk_id"],
                "snippet": c["snippet"]
            }
            for c in chunks
        ]
        
        return {"issue_type": issue_type,"chunks": cleaned_chunks}

    def formatted_context(self, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "No relevant troubleshooting knowledge-base documents found for this domain."
            
        formatted_chunks = []
        for chunk in chunks:
            source = chunk.get("source_file", "unknown")
            chunk_id = chunk.get("chunk_id", "unknown")
            domain = chunk.get("issue_domain", "UNKNOWN")
            score = chunk.get("relevance_score", 0.0)
            snippet = chunk.get("snippet", "")
            
            formatted_chunks.append(
                f"[Source File]: {source}\n"
                f"[Domain]: {domain} | [Chunk ID]: {chunk_id} | [Relevance Score]: {score}\n"
                f"[Snippet]: {snippet}"
            )

        return "\n\n---\n\n".join(formatted_chunks)

    def parallel_policy_retrieval(self, query: str, issue_domains: List[str], top_k: int = TOP_K) -> str:
        all_chunks = []
        for domain in issue_domains:
            domain_chunks = self.retrieve_troubles_chunks(query=query, issue_domain=domain, top_k=top_k)
            all_chunks.extend(domain_chunks)
        all_chunks.sort(key=lambda x: x["relevance_score"], reverse=True)
        return self.formatted_context(all_chunks)