import os
from langchain_core.documents import Document


def load_md_documents(data_folder: str):
    "Load Markdown files from a folder and return a list of Document objects."
    documents = []
    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"Folder not found: {data_folder}")

    md_files = [f for f in os.listdir(data_folder) if f.lower().endswith(".md")]

    if not md_files:
        raise ValueError("No markdown (.md) files found in data/policies")

    for md_file in md_files:
        md_path = os.path.join(data_folder, md_file)
        with open(md_path, "r", encoding="utf-8") as fh:
            content = fh.read()
        metadata = {"source_file": md_file,"document_type": "policy",}

        documents.append(Document(page_content=content,metadata=metadata,))
    return documents