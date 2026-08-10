import hashlib
from typing import List, Dict, Any

from config import CHUNK_SIZE, CHUNK_OVERLAP


def split_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks.

    Chunk size of 1000 characters balances retrieval precision with enough context
    for the LLM to generate a grounded answer. Overlap of 150 characters ensures
    no important information is lost at chunk boundaries (e.g. a sentence or
    bullet point split across two chunks).
    """
    if chunk_size <= chunk_overlap:
        raise ValueError("chunk_size must be greater than chunk_overlap")

    chunks: List[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == text_length:
            break
        start += chunk_size - chunk_overlap
    return chunks


def make_chunk_id(source_file: str, page_number: int, index: int, text: str) -> str:
    prefix = f"{source_file}_p{page_number:03d}_{index:03d}"
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}_{digest}"


def create_chunks(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert a list of document pages into overlapping chunks with metadata.

    Each chunk includes: chunk_id, source_file, page_number, section_title, text.
    The chunk_id is a deterministic hash (SHA-1 prefix) of the text content,
    making it reproducible across runs.
    """
    chunks: List[Dict[str, Any]] = []
    for document in documents:
        source_file = document["source_file"]
        page_number = document.get("page_number", 1)
        section_title = document.get("section_title", "")
        text = document["text"]
        raw_chunks = split_text(text)

        for index, chunk_text in enumerate(raw_chunks, start=1):
            chunk_id = make_chunk_id(source_file, page_number, index, chunk_text)
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "source_file": source_file,
                    "page_number": page_number,
                    "section_title": section_title,
                    "text": chunk_text,
                }
            )
            # Metadata enables source tracking for citations and grounding.
    return chunks