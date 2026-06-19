import config
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

def get_vectorstore(chunks=None, persist_dir=config.VECTOR_STORE_PATH):
    if chunks:
        return Chroma.from_documents(chunks, embedding, persist_directory=persist_dir)
    return Chroma(persist_directory=persist_dir, embedding_function=embedding)

def retrieve(vectorstore, query, domain=None, k=config.TOP_K):
    if domain:
        results = vectorstore.similarity_search_with_score(query, k=k*3)
        results = [(d, s) for d, s in results if d.metadata.get("KB_domain","").lower() == domain.lower()]
        return results[:k]
    return vectorstore.similarity_search_with_score(query, k=k)

def retreive_emai_trouble_shooting_guide(vectorstore, query, k=config.TOP_K):
    return retrieve(vectorstore, query, domain="EMAIL_OUTLOOK_TROBLESHOOTING_GUIDE", k=k)

def laptop(vectorstore, query, k=config.TOP_K):
    return retrieve(vectorstore, query, domain="LAPTOP_PERFORMANCE_GUIDE", k=k)

def network(vectorstore, query, k=config.TOP_K):
    return retrieve(vectorstore, query, domain="NETWORK_CONNECTIVITY_GUIDE", k=k)

def password(vectorstore, query, k=config.TOP_K):
    return (vectorstore, query, domain=" PASSWORD_RESET_GUIDE", k=k)

def printer(vectorstore, query, k=config.TOP_K):
    return retrieve(vectorstore, query, domain="PRINTER_TROUBLESHOOTING_GUIDE", k=k)
def VPN(vectorstore, query, k=config.TOP_K):
    return retrieve(vectorstore, query, domain="VPN_TROUBLESHOOTING_GUIDE", k=k)