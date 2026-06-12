from config import TOP_K
from run import vector_store

def retrieve_documents(vector_store,query):
    retriever = vector_store.as_retriever(
        searc_type="similarity",
        search_kwargs={"k": TOP_K})
    return retriever.invoke(query)