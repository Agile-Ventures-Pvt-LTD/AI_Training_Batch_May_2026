from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from config import VECTOR_STORE_PATH, EMBEDDING_MODEL, TOP_K
from loaders import load_documents, split_documents


def get_vector_store():
    docs = load_documents()
    chunks = split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    chromadb_client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
    
    vector_db = Chroma(
        collection_name="issue-chunks",
        embedding_function=embeddings,
        client=chromadb_client,
        persist_directory=VECTOR_STORE_PATH,
    )
    
    if vector_db._collection.count() == 0:
        vector_db.add_documents(documents=chunks, ids=[f"chunk_{i}" for i in range(len(chunks))])
    
    return vector_db.as_retriever(search_type="similarity", search_kwargs={"k": TOP_K})
