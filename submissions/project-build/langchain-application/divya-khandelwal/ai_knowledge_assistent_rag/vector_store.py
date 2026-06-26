import time
import chromadb
from langchain_chroma import Chroma

from embedding import embedding
from chunking import chunking
from loaders import pdf_loader


def create_db():

    # Load PDF
    load_pdf = pdf_loader()
    print("pdf loaded")

    # Create chunks
    chunks = chunking(load_pdf)
    print("chunks created")
    print("Total chunks:", len(chunks))


    # Create embeddings
    embeddings = embedding()
    print("embedding done")


    # Chroma database configuration
    collection_name = "amazon-10k-2025"

    chromadb_client = chromadb.PersistentClient(
        path="./amazon_db"
    )


    vectorstore_persistent = Chroma(
        collection_name=collection_name,
        collection_metadata={
            "hnsw:space": "cosine"
        },
        embedding_function=embeddings,
        client=chromadb_client,
        persist_directory="./amazon_db"
    )


    # Add documents in batches
    batch_size = 500

    for i in range(0, len(chunks), batch_size):

        batch_chunks = chunks[i:i + batch_size]

        ids = [
            "text_" + str(index)
            for index in range(i, i + len(batch_chunks))
        ]

        vectorstore_persistent.add_documents(
            documents=batch_chunks,
            ids=ids
        )

        print(
            f"Added chunks {i} to {i + len(batch_chunks)}"
        )

        time.sleep(2)


    print("Vector database created successfully")

    return vectorstore_persistent



if __name__ == "__main__":

    vector_store = create_db()

    print("vector db done")