import os
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import config

class Vectorstore:
    def __init__(self):
        self.embeddings=HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={"local_files_only": True}
        )
        self.chromadb_client=chromadb.PersistentClient(
            path=config.VECTOR_PATH
        )
        self.vector_store=Chroma(
            collection_name="policy-collection",
            collection_metadata={"hnsw:space":"cosine"},
            embedding_function=self.embeddings,
            client=self.chromadb_client,
            persist_directory=config.VECTOR_PATH
        )
    def create_vector(self, chunks):
        self.vector_store.add_documents(chunks)
        return self.vector_store
    
    def get_retriever(self, search_kwargs=None):
        if search_kwargs is None:
            search_kwargs={"k":config.TOP_K}
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
    
    def retrieve_domain(self,query,domain,k=config.TOP_K):
        result=self.vector_store.similarity_search(
            query,k=k, filter={"policy_domain":domain}
        )
        return result