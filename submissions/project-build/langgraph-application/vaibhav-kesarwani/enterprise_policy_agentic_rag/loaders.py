import time
from langchain_chroma import Chroma
from chunking import policies_chunks
from config import chromadb_client, embedding

vectorstore = Chroma(
    collection_name="policies",
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding,
    client=chromadb_client,
    persist_directory="./vector_store"
)


def document_storing(policies_chunks):
    i = 0 

    while i < len(policies_chunks):
        vectorstore.add_documents( 
            documents = policies_chunks[i : i + 500],
            ids=["text_" + str(i) for i in range(i, i + 500)] 
        )

        i += 500
        time.sleep(5)


document_storing(policies_chunks)