from config import TOP_K
def get_retriever(vectorstore):

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K
        }
    )

    return retriever

def search_knowledge_base(query: str, retriever):
    """Executes a search query against the retriever and returns matching chunks."""
    # Invokes the retriever to get relevant chunks
    matching_docs = retriever.invoke(query)
    return matching_docs