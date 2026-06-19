import os
import re
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from config import VECTOR_STORE_PATH,CHUNK_SIZE,CHUNK_OVERLAP

SUPPORTED_FILES = [".pdf", ".txt", ".md"]

def extract_issue_domain(filename: str) -> str:
    clean_name = filename.lower()
    if "vpn" in clean_name:
        return "vpn"
    elif "email" in clean_name or "outlook" in clean_name:
        return "outlook_email"
    elif "laptop" in clean_name or "performance" in clean_name:
        return "laptop_performance"
    elif "password" in clean_name or "reset" in clean_name:
        return "password_reset"
    elif "network" in clean_name or "connectivity" in clean_name:
        return "network_connectivity"
    elif "printer" in clean_name:
        return "printer"
    return "unknown"

def load_documents(folder_path: str) -> List[Document]:
    documents = []
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"{folder_path} does not exist")

    for file in folder.iterdir():
        if file.suffix.lower() not in SUPPORTED_FILES:
            continue
        try:
            if file.suffix == ".pdf":
                loader = PyPDFLoader(str(file))
            elif file.suffix == ".md":
                loader = TextLoader(str(file), encoding="utf-8") 
            else:
                loader = TextLoader(str(file))
            docs = loader.load()

            for doc in docs:
                doc.metadata["source_file"] = file.name
                doc.metadata["issue_domain"] = extract_issue_domain(file.name)
                doc.page_content = doc.page_content
            documents.extend(docs)

        except Exception as e:
            print(f"Failed loading {file}: {e}")

    return documents

def chunk_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    processed_chunks = []

    for idx, chunk in enumerate(chunks):
        metadata = chunk.metadata.copy()
        metadata["chunk_id"] = f"chunk_{idx:05d}"
        metadata["text"] = chunk.page_content
        chunk.metadata = metadata
        processed_chunks.append(chunk)

    return processed_chunks

def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))

def create_vector_store(chunks: List[Document]) -> Chroma:
    embeddings = get_embedding_model()
    vector_store = Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory=VECTOR_STORE_PATH)
    return vector_store

def load_vector_store() -> Chroma:
    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError(f"Vector Store directory not found at {VECTOR_STORE_PATH}")
    
    embeddings = get_embedding_model()
    return Chroma( persist_directory=VECTOR_STORE_PATH,embedding_function=embeddings)