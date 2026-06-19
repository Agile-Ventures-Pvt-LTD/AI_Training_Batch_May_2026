# from config import TOP_K
# from typing import Dict, Any,List
# class Retriever:
#     def __init__(self, vector_store):
#         self.vector_store = vector_store

#     def retrieve_policies_chunks(self,query: str,policy_domain: str,top_k: int = TOP_K)-> List[Dict]:

#        results = self.vector_store.similarity_search_with_relevance_scores(query=query,k=top_k,filter={"policy_domain": policy_domain} )
#        retrieved_chunks = []
#        for doc, score in results:
#             retrieved_chunks.append(
#                 {
#                     "policy_domain": doc.metadata.get("policy_domain"),
#                     "source_file": doc.metadata.get("source_file"),
#                     "chunk_id": doc.metadata.get("chunk_id"),
#                     "content": doc.page_content,
#                     "relevance_score": round(float(score),2)
#                 }
#             )

#        return retrieved_chunks

#     def formatted_context(docs):
#         formatted_chunks = []
#         for doc in docs:
#             source = doc.metadata.get("source_file","unknown")
#             chunk_id = doc.metadata.get("chunk_id","unknown")
#             formatted_chunks.append(f"Source: {source}Chunk: {chunk_id}{doc.page_content}")

#         return "\n\n".join(formatted_chunks)

#     def parallel_policy_retrieval(retrieve_policies_chunks,query: str,policy_domains: List[str],top_k: int = TOP_K) -> List[Dict]:

#         all_chunks = []
#         for domain in policy_domains:
#             domain_chunks = retrieve_policies_chunks(query=query,policy_domain=domain,top_k=top_k)
#             all_chunks.extend(domain_chunks)

#         all_chunks.sort(key=lambda x: x["relevance_score"],reverse=True)

#         return all_chunks
    

from config import TOP_K
from typing import Dict, Any, List

class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve_policies_chunks(self, query: str, policy_domain: str, top_k: int = TOP_K) -> List[Dict]:
        print(f"-> [Retriever] Fetching from domain '{policy_domain}' for query: '{query}'")
        
        results = self.vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=top_k,
            filter={"policy_domain": policy_domain}
        )
        
        retrieved_chunks = []
        for doc, score in results:
            retrieved_chunks.append({
                "policy_domain": doc.metadata.get("policy_domain"),
                "source_file": doc.metadata.get("source_file"),
                "chunk_id": doc.metadata.get("chunk_id"),
                "content": doc.page_content,
                "relevance_score": round(float(score), 2)
            })

        return retrieved_chunks

    def formatted_context(self, chunks: List[Dict]) -> str:

        if not chunks:
            return "No relevant policy documents found for this domain."
            
        formatted_chunks = []
        for chunk in chunks:
            source = chunk.get("source_file", "unknown")
            chunk_id = chunk.get("chunk_id", "unknown")
            domain = chunk.get("policy_domain", "UNKNOWN")
            score = chunk.get("relevance_score", 0.0)
            content = chunk.get("content", "")
            
            formatted_chunks.append(
                f"[Source File]: {source}\n"
                f"[Domain]: {domain} | [Chunk ID]: {chunk_id} | [Relevance Score]: {score}\n"
                f"[Content]: {content}"
            )

        return "\n\n---\n\n".join(formatted_chunks)

    def parallel_policy_retrieval(self, query: str, policy_domains: List[str], top_k: int = TOP_K) -> str:
        all_chunks = []
        for domain in policy_domains:
            domain_chunks = self.retrieve_policies_chunks(query=query, policy_domain=domain, top_k=top_k)
            all_chunks.extend(domain_chunks)

        all_chunks.sort(key=lambda x: x["relevance_score"], reverse=True)

        return self.formatted_context(all_chunks)
