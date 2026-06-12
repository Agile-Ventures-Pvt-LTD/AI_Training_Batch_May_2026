from vector_store import vectorstore

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)
