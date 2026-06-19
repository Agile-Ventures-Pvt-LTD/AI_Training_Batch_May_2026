from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = []
    for doc in documents:
        split_docs = splitter.split_documents([doc])
        
        for idx, chunk in enumerate(split_docs):
            chunk.metadata["chunk_id"] = f"{doc.metadata['source_file']}_chunk_{idx:03d}"
            chunk.metadata["chunk_index"] = idx
            chunks.append(chunk)
    return chunks

def add_chunk_metadata(chunks):
    for chunk in chunks:
        source = chunk.metadata.get("source_file", "unknown")
        domain = chunk.metadata.get("issue_domain", "UNKNOWN")
        
        chunk.metadata["source_context"] = {
            "domain": domain,
            "file": source,
            "preview": chunk.page_content[:100].replace("\n", " ")
        }
    return chunks
