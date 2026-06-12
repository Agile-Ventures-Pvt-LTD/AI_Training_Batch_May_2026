import os
import time
import chromadb
from dotenv import load_dotenv
from embeddings import embedding
from chunking import amazon_chunks
from langchain_chroma import Chroma

load_dotenv()
os.environ["DB_PATH"] = os.getenv("DB_PATH")

# Chromadb Client
amazon_collection = "amazon_collection-2025"
chromadb_client = chromadb.PersistentClient(
    path=os.environ["DB_PATH"]
)

# Amazon Vector DB
vectorstore = Chroma(
    collection_name=amazon_collection,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding,
    client=chromadb_client,
    persist_directory=os.environ["DB_PATH"]
)

print(chromadb_client.list_collections())


# Putting the chunks into the vector database
i = 0

while i < len(amazon_chunks):
    vectorstore.add_documents(
        documents=amazon_chunks[i : i + 500],
        ids=["text_" + str(i) for i in range(i, i + 500)]
    )

    i += 500
    time.sleep(5)