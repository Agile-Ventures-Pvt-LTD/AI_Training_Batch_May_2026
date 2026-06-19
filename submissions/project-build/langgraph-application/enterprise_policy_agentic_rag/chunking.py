from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []

    for doc in docs:
        split_texts = splitter.split_text(doc["text"])

        for i, chunk in enumerate(split_texts):
            chunks.append({
                "chunk_id": f"{doc['source_file']}_{i}",
                "text": chunk,
                "source_file": doc["source_file"],
                "policy_domain": doc["policy_domain"]
            })

    return chunks