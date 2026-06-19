import chromadb
import config
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loaders import load_kb

class ChromaRetriever:    
    def __init__(self, persist_dir= None, model_name = None):
        self.persist_dir = config.VECTOR_STORE_PATH
        self.model_name = config.EMBEDDING_MODEL
        
        self.embedding = HuggingFaceEmbeddings(model_name=self.model_name)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.vectorstore = Chroma(
            collection_name="it_support_kb",
            collection_metadata={"hnsw:space": "cosine"},
            embedding_function=self.embedding,
            client=self.client,
            persist_directory=self.persist_dir)
    def add_documents(self, docs):
        existing_ids = set(self.vectorstore.get(include=[])["ids"])
            
        new_docs = [d for d in docs if d["metadata"]["chunk_id"] not in existing_ids]
        if new_docs:
            self.vectorstore.add_texts(
                texts=[d["content"] for d in new_docs],
                metadatas=[d["metadata"] for d in new_docs],
                ids=[d["metadata"]["chunk_id"] for d in new_docs])

    def similarity_search(self, query, k = 4, filter_domain= None):
        k = k
        search_filter = {"issue_domain": filter_domain} if filter_domain else None
        results = self.vectorstore.similarity_search_with_relevance_scores(query, k=k, filter=search_filter)
        return [
            {"content": doc.page_content, "metadata": doc.metadata, "score": float(score)}
            for doc, score in results]

retriever = None
def get_retriever() -> ChromaRetriever:
    global retriever
    if retriever is None:
        retriever = ChromaRetriever()
        retriever.add_documents(load_kb(config.KB_PATH))
    return retriever
