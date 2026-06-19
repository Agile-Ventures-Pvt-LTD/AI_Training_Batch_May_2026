from config import TOP_K
from embeddings import get_embedding_model
from langchain_chroma import Chroma
from config import DB_PATH
import chromadb


embedding_model = get_embedding_model()
chromadb_client = chromadb.Client()
vectorstore = Chroma(
    collection_name="policies",
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding_model,
    client=chromadb_client,
    persist_directory=DB_PATH
)

def retrieve_documents(vector_store,query):
    retriever = vector_store.as_retriever(
        searc_type="similarity",
        search_kwargs={"k": TOP_K})
    return retriever.invoke(query)