from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import (VECTOR_STORE_PATH,TOP_K,EMBEDDING_MODEL)
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
class VectorStoreManager:
    def __init__(self):
        self.vector_store = None
    def create_vector_store(self,documents):
        self.vector_store = Chroma.from_documents(documents=documents,embedding=embedding_model,persist_directory=VECTOR_STORE_PATH)
        print(f"Vector Store Created ({len(documents)} chunks)")
        return self.vector_store
    def load_vector_store(self):
        self.vector_store = Chroma(persist_directory=VECTOR_STORE_PATH,embedding_function=embedding_model)
        return self.vector_store
    def similarity_search(self,query,k=TOP_K):
        if self.vector_store is None:
            self.load_vector_store()
        return self.vector_store.similarity_search(query,k=k)
vector_store = VectorStoreManager()
def retrieve_documents(query,domains=None):
    docs = vector_store.similarity_search(query)
    if not domains:
        return docs
    filtered = []
    for doc in docs:
        if doc.metadata.get("policy_domain") in domains:
            filtered.append(doc)
    return filtered

def retrieve_hr_policy(query):
    return retrieve_documents(query,["HR_LEAVE"])
def retrieve_travel_policy(query):
    return retrieve_documents(query,["TRAVEL"])
def retrieve_reimbursement_policy(query):
    return retrieve_documents(query, ["REIMBURSEMENT"])
def retrieve_it_security_policy(query):
    return retrieve_documents(query,["IT_SECURITY"])

def retrieve_ai_usage_policy(query):
    return retrieve_documents(query,["AI_USAGE"])