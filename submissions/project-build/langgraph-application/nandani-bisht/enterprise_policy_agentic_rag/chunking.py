import hashlib
import logging
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config

logger = logging.getLogger(__name__)


def _chunk_id(source_file: str, index: int) -> str:
    return hashlib.md5(f"{source_file}_{index}".encode()).hexdigest()[:12]


def chunk_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    all_chunks = []
    for doc in documents:
        source_file = doc.metadata.get("source_file", "unknown")
        domain = doc.metadata.get("policy_domain", "OTHER")

        splits = splitter.split_documents([doc])
        for chunk in splits:
            idx = len(all_chunks)
            chunk.metadata["chunk_id"] = _chunk_id(source_file, idx)
            chunk.metadata["source_file"] = source_file
            chunk.metadata["policy_domain"] = domain
            all_chunks.append(chunk)

    logger.info("Created %d chunks from %d documents", len(all_chunks), len(documents))
    return all_chunks
