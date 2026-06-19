import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from config import chromadb_client, embedding

load_dotenv()
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")

try:
    policies_store = Chroma(
        collection_name="policies",
        collection_metadata={"hnsw:space": "cosine"},
        embedding_function=embedding,
        client=chromadb_client,
        persist_directory="./vector_store"
    )

    retriever = policies_store.as_retriever(
        search_type='similarity',
        search_kwargs={'k': 5}
    )
except Exception as e:
    print(e)