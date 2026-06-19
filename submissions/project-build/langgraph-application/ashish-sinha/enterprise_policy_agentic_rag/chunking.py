from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL
import os
from langchain_chroma import Chroma
from config import VECTOR_STORE_PATH
from config import (CHUNK_SIZE,CHUNK_OVERLAP)

def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)
    processed_chunks = []

    for idx, chunk in enumerate(chunks):
        metadata = chunk.metadata.copy()
        metadata["chunk_id"] = (f"chunk_{idx:05d}")
        metadata["source_file"] = (metadata.get("source_file","").split(".")[-1])
        # if "pocily_domain" in metadata:
        #     metadata["policy_domain"] = metadata["policy_domain"]
        metadata["policy_domain"] = metadata.get("policy_domain","")
        metadata["text"] = (metadata.get("text","Unknown"))
        chunk.metadata = metadata
        processed_chunks.append(chunk)

    return processed_chunks

def get_embedding_model():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings

def create_vector_store(chunks):
    embeddings =  get_embedding_model()
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding= embeddings,
        persist_directory= VECTOR_STORE_PATH
    )
    return vector_store

def load_vector_store():
    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError("Vector Store not FOund")
    embeddings = get_embedding_model()

    return Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )