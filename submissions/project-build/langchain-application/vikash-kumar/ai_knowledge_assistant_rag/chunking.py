import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (CHUNK_SIZE,CHUNK_OVERLAP)

def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

    chunks = splitter.split_documents(documents)

    for idx, chunk in enumerate(chunks):
       chunk.metadata["chunk_id"] = (f"chunk_{idx:05d}")
    
    return chunks

