from langchain_chroma import Chroma

def init_retriever(collection, embedding, chromadb_client, directory, search_kwargs=None):
    """Initialize a retriever from a Chroma vector store. Returns LangChain retriever object."""
    try:
        vectorstore = Chroma(
            collection_name=collection,
            collection_metadata={"hnsw:space": "cosine"},
            embedding_function=embedding,
            client=chromadb_client,
            persist_directory=directory
        )
        retriever = vectorstore.as_retriever(search_type='similarity',search_kwargs=search_kwargs or {"k": 3})
        return retriever
    except Exception as e:
        raise RuntimeError(f"Failed to initialize retriever: {e}")


def query_retriever(retriever, query):
    """
    Query the retriever for similar documents.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    try:
        results = retriever.invoke(query)
        if not results:
            raise ValueError("No results found for the query.")
        return results
    except Exception as e:
        raise RuntimeError(f"Retriever query failed: {e}")

