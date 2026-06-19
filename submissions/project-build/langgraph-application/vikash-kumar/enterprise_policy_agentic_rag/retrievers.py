from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL,VECTOR_STORE_PATH,TOP_K

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def build_vector_store(chunks):
    """It will build the vector store"""
    vector_store = Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory=VECTOR_STORE_PATH)
    return vector_store

def load_vector_store():
    """THis will load the vectore store"""
    return Chroma(persist_directory=VECTOR_STORE_PATH,embedding_function=embeddings)

def retrieve_by_domain(question,policy_domain):
    "THis will retreive by domain"
    vector_store = load_vector_store()
    docs = vector_store.similarity_search(query=question,k=TOP_K,filter={"policy_domain": policy_domain})
    return docs

def retrieve_policies(question,policy_domains):
    """This will retrieve the policies"""
    retrieved_docs = []
    for domain in policy_domains:
        docs = retrieve_by_domain(question,domain)
        retrieved_docs.extend(docs)
    return retrieved_docs