import time
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain_chroma import Chroma

from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (CHUNK_SIZE,CHUNK_OVERLAP)

def chunk_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = text_splitter.split_documents(documents)

    processed_chunks = []

    for idx, chunk in enumerate(chunks):

        metadata = chunk.metadata.copy()

        metadata["chunk_id"] = (f"chunk_{idx:05d}")

        metadata["document_type"] = (metadata.get("source_file","").split(".")[-1])

        if "page" in metadata:
            metadata["page_number"] = metadata["page"]

        metadata["section_title"] = (metadata.get("section_title","Unknown"))

        chunk.metadata = metadata

        processed_chunks.append(chunk)

    return processed_chunks