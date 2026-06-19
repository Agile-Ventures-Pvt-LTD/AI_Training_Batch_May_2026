import config
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

def get_vectorstore(chunks=None, persist_dir=config.VECTOR_STORE_PATH):
    if chunks:
        return Chroma.from_documents(chunks, embedding, persist_directory=persist_dir)
    return Chroma(persist_directory=persist_dir, embedding_function=embedding)

def retrieve_policy(vectorstore, query, domain=None, k=config.TOP_K):
    if domain:
        results = vectorstore.similarity_search_with_score(query, k=k*3)
        results = [(d, s) for d, s in results if d.metadata.get("policy_domain","").lower() == domain.lower()]
        return results[:k]
    return vectorstore.similarity_search_with_score(query, k=k)

def retrieve_hr_policy(vectorstore, query, k=config.TOP_K):
    return retrieve_policy(vectorstore, query, domain="HR_LEAVE", k=k)

def retrieve_travel_policy(vectorstore, query, k=config.TOP_K):
    return retrieve_policy(vectorstore, query, domain="TRAVEL", k=k)

def retrieve_reimbursement_policy(vectorstore, query, k=config.TOP_K):
    return retrieve_policy(vectorstore, query, domain="REIMBURSEMENT", k=k)

def retrieve_it_security_policy(vectorstore, query, k=config.TOP_K):
    return retrieve_policy(vectorstore, query, domain="IT_SECURITY", k=k)

def retrieve_ai_usage_policy(vectorstore, query, k=config.TOP_K):
    return retrieve_policy(vectorstore, query, domain="AI_USAGE", k=k)