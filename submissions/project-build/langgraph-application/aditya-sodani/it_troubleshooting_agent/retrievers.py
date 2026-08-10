import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import *


def create_retriever(documents):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(VECTOR_STORE_PATH) and os.listdir(VECTOR_STORE_PATH):
        print("Loading existing vector store...")

        vectordb = Chroma(
            persist_directory=VECTOR_STORE_PATH,
            embedding_function=embeddings
        )

    else:
        print("Creating new vector store (first run only)...")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        chunks = splitter.split_documents(documents)

        vectordb = Chroma.from_documents(
            chunks,
            embedding=embeddings,
            persist_directory=VECTOR_STORE_PATH
        )

        vectordb.persist()

    return vectordb.as_retriever(search_kwargs={"k": TOP_K})