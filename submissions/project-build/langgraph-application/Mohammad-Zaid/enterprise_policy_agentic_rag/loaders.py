import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

POLICIES_FOLDER = "./data/policies"

def load_documents(folder_path=POLICIES_FOLDER):
    docs = []
    if not os.path.exists(folder_path):
        return docs
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            try:
                loader = TextLoader(file_path, encoding="utf-8")
                loaded_docs = loader.load()
                for i, doc in enumerate(loaded_docs, start=1):
                    source_path = Path(file_path)
                    doc.metadata = {
                        "source_file": source_path.name,
                        "policy_domain": source_path.stem,
                        "page_number": str(i),
                    }
                    docs.append(doc)
            except Exception as e:
                continue
    return docs
