from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

def chunk_documents(documents, chunk_size, chunk_overlap):
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)

    with open(
        "outputs.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    return chunks