from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

def split_and_set_metadata(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunk_documents = text_splitter.split_documents(docs)
    chunks = []
    for i, chunk_document in enumerate(chunk_documents, start=1):
        metadata = dict(chunk_document.metadata)
        metadata["chunk_id"] = f"chunk_{i}"
        chunks.append(
            Document(
                page_content=chunk_document.page_content,
                metadata=metadata
            )
        )
    return chunks
