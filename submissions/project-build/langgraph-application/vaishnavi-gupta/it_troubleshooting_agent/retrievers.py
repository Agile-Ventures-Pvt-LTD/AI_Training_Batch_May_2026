retriever = vectorstore_persisted.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 4}
)

