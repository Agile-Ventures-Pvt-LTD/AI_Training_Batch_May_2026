from typing import List
from langchain_core.documents import Document
from vector_store import VectorStoreManager

class RetrieverManager:
    def __init__(self, vector_store_manager: VectorStoreManager, top_k: int = 5):
        self.vector_store_manager = vector_store_manager
        self.top_k = top_k

    def retrieve(self, query):
        retriever=self.vector_store_manager.get_retriever(search_kwargs={"k":self.top_k})
        return retriever.invoke(query)
    
    def get_debug_info(self, query, docs):
        debug_info = {
            "question": query,
            "top_k": self.top_k,
            "retrieved_chunks": []
        }
        for i, doc in enumerate(docs):
            debug_info["retrieved_chunks"].append({
                "rank": i + 1,
                "chunk_id": doc.metadata.get("chunk_id", "N/A"),
                "source_file": doc.metadata.get("source_file", "N/A"),
                "page_number": doc.metadata.get("page_number", "N/A"),
                "preview": doc.page_content[:200] + "..."
            })
        return debug_info