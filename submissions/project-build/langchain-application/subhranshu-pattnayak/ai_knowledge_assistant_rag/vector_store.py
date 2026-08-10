import time
from langchain_chroma import Chroma

def load_chunks(collection, embedding, chromadb_client, directory, chunks):
    """Persist chunks into a Chroma vector store with batching and error handling."""
    if not chunks:
        raise ValueError("No chunks provided for vector store loading.")

    try:
        vectorstore = Chroma(
            collection_name=collection,
            collection_metadata={"hnsw:space": "cosine"},
            embedding_function=embedding,
            client=chromadb_client,
            persist_directory=directory
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Chroma vector store: {e}")

    i = 0
    errors = []

    while i < len(chunks):
        batch = chunks[i:i+20]
        try:
            vectorstore.add_documents(
                documents=batch,
                ids=[f"text_{j}" for j in range(i, i+len(batch))]
            )
        except Exception as e:
            errors.append(f"Batch {i}-{i+len(batch)} failed: {e}")
        i += 20
        time.sleep(5)

    if errors:
        print("Errors occurred while adding documents:")
        for err in errors:
            print(f" - {err}")

    if i == 0:
        raise RuntimeError("No documents were successfully added to the vector store.")