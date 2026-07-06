import os
from typing import Optional

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.config import (KNOWLEDGE_BASE_PATH,EMBEDDING_MODEL,CHUNK_SIZE,CHUNK_OVERLAP,TOP_K,FAISS_SAVE_DIR)

retriever_instance = None
vector_store_instance = None


def build_vector_store():
    global vector_store_instance
    if vector_store_instance is not None:
        return vector_store_instance
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    if os.path.exists(FAISS_SAVE_DIR) and os.path.exists(os.path.join(FAISS_SAVE_DIR, "index.faiss")):
        vector_store_instance = FAISS.load_local(folder_path=FAISS_SAVE_DIR,
            embeddings=embeddings,
            allow_dangerous_deserialization=True 
        )
        return vector_store_instance
    loader = TextLoader(str(KNOWLEDGE_BASE_PATH), encoding="utf-8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = text_splitter.split_documents(documents)
    vector_store_instance = FAISS.from_documents(chunks, embeddings)
    vector_store_instance.save_local(folder_path=FAISS_SAVE_DIR)
    
    return vector_store_instance


def get_retriever():
    global retriever_instance
    if retriever_instance is not None:
        return retriever_instance

    vector_store = build_vector_store()
    retriever_instance = vector_store.as_retriever(
        search_kwargs={"k": TOP_K}
    )
    return retriever_instance


def retrieve_logistics_rules(query: str, retriever=None) -> str:
    active_retriever = retriever if retriever is not None else get_retriever()
    docs = active_retriever.invoke(query)
    return "\n\n".join(doc.page_content for doc in docs)


def set_retriever_for_testing(mock_retriever):
    global retriever_instance
    retriever_instance = mock_retriever


def reset_retriever():
    global retriever_instance, vector_store_instance
    retriever_instance = None
    vector_store_instance = None