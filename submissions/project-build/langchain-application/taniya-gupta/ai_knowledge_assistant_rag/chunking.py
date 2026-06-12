import re 
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkingManager:
    def __init__(self, chunk_size=1000, chunk_overlap=150):
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        self.text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def split_documents(self, documents):
        for doc in documents:
            doc.page_content = re.sub(r'\s+', ' ', doc.page_content).strip()
        chunks=self.text_splitter.split_documents(documents)
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"]=f"chunk_{i:04d}"
            if "source" in chunk.metadata:
                chunk.metadata["source_file"] = os.path.basename(chunk.metadata["source"])
            if "page" in chunk.metadata:
                chunk.metadata["page_number"] = chunk.metadata.get("page", 0) +1
        return chunks
    
def split_documents(documents, chunk_size=1000, chunk_overlap=150):
    manager=ChunkingManager(chunk_size, chunk_overlap)
    return manager.split_documents(documents)