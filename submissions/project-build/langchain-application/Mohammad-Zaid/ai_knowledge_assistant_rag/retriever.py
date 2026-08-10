
import os


def retrieve_documents(vector_db, query, top_k=None):
    if top_k is None:
        top_k = int(os.getenv("TOP_K", "5"))
    
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )
    return retriever.invoke(query)


def build_context_from_documents(documents):
    return "\n\n".join([doc.page_content for doc in documents])


def build_citations_from_documents(documents):
    return [f"Source: {doc.metadata['source_file']} (Page {doc.metadata['page_number']})" 
            for doc in documents]
