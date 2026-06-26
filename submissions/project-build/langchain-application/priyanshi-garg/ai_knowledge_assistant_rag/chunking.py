from loaders import load_documents

from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)
from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

chunks = load_documents.load_and_split(splitter)

print(
    f"Total Chunks Created: {len(chunks)}"
)