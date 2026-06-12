from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(docs: list) -> list:
    docs = [d for d in docs if d.page_content.strip()]
    print(f"[INFO] Non-empty pages: {len(docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata = {
            "chunk_id": f"chunk_{i:04d}",
            "source_file": Path(chunk.metadata.get("source", "")).name,
            "page": chunk.metadata.get("page", 0),
        }

    print(f"Created {len(chunks)} chunks from {len(docs)} pages")
    return chunks