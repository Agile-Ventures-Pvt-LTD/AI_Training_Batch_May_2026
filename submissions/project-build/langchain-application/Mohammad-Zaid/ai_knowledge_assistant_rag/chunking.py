
import re
import os
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_document(text):
    lines = [" ".join(line.split()) for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def set_document_metadata(document, file_path, chunk_id=""):
    source_file = Path(file_path).name
    year_match = re.search(r"(19|20)\d{2}", source_file)
    year = year_match.group(0) if year_match else ""
    metadata = dict(document.metadata or {})
    page_number = metadata.get("page_number")
    if page_number is None:
        page = metadata.get("page")
        page_number = page + 1 if isinstance(page, int) else metadata.get("page_label") or 1
    if isinstance(page_number, str) and page_number.isdigit():
        page_number = int(page_number)
    metadata.update(
        {
            "source_file": source_file,
            "page_number": page_number,
            "document_type": "pdf",
            "year": year,
            "chunk_id": chunk_id,
        }
    )
    return Document(page_content=clean_document(document.page_content), metadata=metadata)


def chunk_documents(documents, chunk_size=None, chunk_overlap=None):
    if chunk_size is None:
        chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
    if chunk_overlap is None:
        chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "150"))
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunk_documents_list = text_splitter.split_documents(documents)
    chunks = []

    for i, chunk_document in enumerate(chunk_documents_list, start=1):
        metadata = dict(chunk_document.metadata or {})
        metadata["chunk_id"] = f"chunk_{i}"
        metadata["text"] = chunk_document.page_content
        chunks.append(Document(page_content=chunk_document.page_content, metadata=metadata))

    print(f"Loaded {len(documents)} cleaned pages.")
    print(f"Total chunks after splitting: {len(chunks)}")
    return chunks
