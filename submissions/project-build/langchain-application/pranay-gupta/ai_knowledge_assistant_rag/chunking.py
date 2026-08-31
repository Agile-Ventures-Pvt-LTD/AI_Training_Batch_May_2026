import json
import os

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    PROCESSED_DATA_PATH
)


def clean_text(text: str) -> str:
    
    # Basic preprocessing.
    
    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )

    processed_docs = []

    chunk_counter = 1

    for document in documents:

        cleaned_text = clean_text(document.page_content)

        chunks = splitter.split_text(cleaned_text)

        for chunk in chunks:

            metadata = document.metadata.copy()

            metadata["chunk_id"] = (
                f"chunk_{chunk_counter:05d}"
            )

            processed_docs.append(
                {
                    "text": chunk,
                    "metadata": metadata
                }
            )

            chunk_counter += 1

    return processed_docs


def save_chunks(chunks):

    os.makedirs(PROCESSED_DATA_PATH,exist_ok=True)

    path = os.path.join(PROCESSED_DATA_PATH,"chunks.json")

    with open(path,"w",encoding="utf-8") as file:

        json.dump(chunks,file,indent=2,ensure_ascii=False)

    print(f"Saved {len(chunks)} chunks")