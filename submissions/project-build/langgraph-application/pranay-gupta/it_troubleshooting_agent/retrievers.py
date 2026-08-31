from config import TOP_K

def create_rag_retriever(vector_store):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )
    return retriever


def retrieve_troubleshooting(retriever, query, issue_type=None):
    results = retriever.invoke(query)
    retrieved_data = []
    for doc in results:
        retrieved_data.append({
            "source_file": doc.metadata.get("source_file", "unknown"),
            "issue_domain": doc.metadata.get("issue_domain", "UNKNOWN"),
            "chunk_id": doc.metadata.get("chunk_id", "unknown"),
            "content": doc.page_content,
            "preview": doc.page_content[:150].replace("\n", " ")
        })
    return retrieved_data


def format_retrieval_results(retrieved_docs):
    if not retrieved_docs:
        return "No relevant troubleshooting guidance found."
    formatted = []
    for idx, doc in enumerate(retrieved_docs, 1):
        formatted.append(f"\n[Source {idx}: {doc['source_file']}]")
        formatted.append(doc['content'])
    
    return "\n".join(formatted)
