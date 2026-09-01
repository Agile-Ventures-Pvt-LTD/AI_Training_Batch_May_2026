from langchain_chroma import Chroma
from embeddings import EmbeddingManager

class VectorStoreManager:
    def __init__(self, persist_directory, model_name):
        self.persist_directory = persist_directory
        self.model_name = model_name
        self.embeddings = EmbeddingManager.get_embeddings(model_name)
        self.vector_store = None

    def create_or_load_vector_store(self, chunks=None):
        if chunks:
            self.vector_store=Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
                )
        else:
            self.vector_store=Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
        return self.vector_store
    def get_retriever(self, search_kwargs=None):
        if not self.vector_store:
            self.create_or_load_vector_store()
        return self.vector_store.as_retriever(search_kwargs=search_kwargs or {})
def get_vector_store(persist_directory, model_name,chunks=None):
    manager=VectorStoreManager(persist_directory, model_name)
    return manager.create_or_load_vector_store(chunks)    
    