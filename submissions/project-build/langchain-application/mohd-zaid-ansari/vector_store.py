import chromadb
import time

from langchain_chroma import Chroma

collection_name = "amazon-10k"
chroma_path = "data/vector_store"


def create_vectorstore(embedding_model):

    chroma_client = chromadb.PersistentClient(
        path=chroma_path
    )

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=chroma_path,
        client=chroma_client,
        collection_metadata={
            "hnsw:space": "cosine"
        }
    )

    return vectorstore


def index_chunks_to_vectorstore(
        chunks,
        vectorstore
):

    i = 0

    while i < len(chunks):

        vectorstore.add_documents(
            documents=chunks[i:i+25],
            ids=[
                f"text_{j}"
                for j in range(
                    i,
                    min(i + 25, len(chunks))
                )
            ]
        )

        print(
            f"Indexed {min(i+25,len(chunks))}/{len(chunks)}"
        )

        i += 25

        time.sleep(5)

    print("Indexing completed.")