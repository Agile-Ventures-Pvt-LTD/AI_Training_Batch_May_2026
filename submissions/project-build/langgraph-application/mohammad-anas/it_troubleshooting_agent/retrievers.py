import os

from langchain_text_splitters import RecursiveCharacterTextSplitter   
from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings

from config import (
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K,
    VECTOR_STORE_PATH
)

from loaders import load_knowledge_base


def create_chunks(documents):
    

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk_{index}"

    return chunks


def build_vector_store():
    

    documents = load_knowledge_base()

    chunks = create_chunks(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH
    )

    return vector_store


def load_vector_store():
   

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )

    return vector_store


def get_retriever():
   

    if not os.path.exists(VECTOR_STORE_PATH):
        build_vector_store()

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": TOP_K
        }
    )

    return retriever