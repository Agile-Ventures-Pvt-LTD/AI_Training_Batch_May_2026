from typing import List
import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import (CHUNK_SIZE,CHUNK_OVERLAP)
def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks.
    Args:
        documents: List of LangChain documents
    Returns:
        List of chunked documents
    """
    if not documents:
        raise ValueError(
            "No documents provided for chunking."
        )
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP,length_function=len,separators=["\n\n","\n",". "," ",""])
    chunks = splitter.split_documents(documents)
    for idx, chunk in enumerate(chunks,start=1):
        chunk.metadata["chunk_id"] = (
            f"chunk_{idx:04d}"
        )
    return chunks

def remove_empty_chunks(chunks: List[Document]) -> List[Document]:
    """
    Remove empty chunks.
    """
    valid_chunks = []
    for chunk in chunks:
        content = (
            chunk.page_content.strip()
            if chunk.page_content
            else ""
        )
        if not content:
            continue
        valid_chunks.append(chunk)
    return valid_chunks
def get_chunk_statistics(chunks: List[Document]) -> dict:
    """
    Return chunking statistics.
    """
    if not chunks:
        return {"total_chunks": 0,"avg_chunk_size": 0,"min_chunk_size": 0,"max_chunk_size": 0}
    sizes = [len(chunk.page_content)for chunk in chunks]
    return {"total_chunks": len(chunks),"avg_chunk_size": round(sum(sizes) / len(sizes),2),"min_chunk_size": min(sizes),"max_chunk_size": max(sizes)}
def print_chunk_summary(
    chunks: List[Document]
):
    """
    Debug helper.
    """
    stats = get_chunk_statistics(chunks)
    print("\nChunk Summary")
    print("-" * 40)
    for key, value in stats.items():
        print(f"{key}: {value}")
    if chunks:
        print("\nSample Chunk Metadata:")
        print(chunks[0].metadata)
        print("\nSample Chunk Content:")
        print(chunks[0].page_content[:300])
if __name__ == "__main__":
    from config import (POLICY_DATA_PATH)
    from loaders import (load_documents,validate_documents)
    docs = load_documents(POLICY_DATA_PATH)
    docs = validate_documents(docs)
    chunks = chunk_documents(docs)
    chunks = remove_empty_chunks(chunks)
    print_chunk_summary(chunks)