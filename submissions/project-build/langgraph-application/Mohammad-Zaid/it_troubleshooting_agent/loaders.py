import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import KB_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents(folder_path=KB_PATH):
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            loader = TextLoader(file_path, encoding="utf-8")
            loaded_docs = loader.load()
            for i, doc in enumerate(loaded_docs, start=1):
                source_path = Path(file_path)
                doc.metadata = {
                    "source_file": source_path.name,
                    "issue_domain": source_path.stem,
                    "page_number": str(i),
                }
                docs.append(doc)
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(docs)
