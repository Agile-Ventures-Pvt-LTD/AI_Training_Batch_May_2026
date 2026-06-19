from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunked_docs = []
    chunk_id = 0
    
    for doc in documents:
        source_file = doc.metadata.get("source_file", "unknown")
        chunks = splitter.split_text(doc.page_content)
        for i, chunk_text in enumerate(chunks):
            chunk_id += 1
            new_doc = Document(
                page_content=chunk_text,
                metadata={
                    "chunk_id": f"chunk_{chunk_id}",
                    "source_file": source_file,
                    "chunk_index": i,
                    "document_type": "policy"
                }
            )
            chunked_docs.append(new_doc)
    
    return chunked_docs

