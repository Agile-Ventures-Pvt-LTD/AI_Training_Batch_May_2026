from langchain_chroma import Chroma

from embedding import embedding
from chunking import chunks

import chromadb
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=chromadb.Settings(anonymized_telemetry=False)
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./chroma_db",
    collection_name="knowledge_base",
    client=client
)

print(
    "Vector DB Created:",
    vectorstore._collection.count()
)