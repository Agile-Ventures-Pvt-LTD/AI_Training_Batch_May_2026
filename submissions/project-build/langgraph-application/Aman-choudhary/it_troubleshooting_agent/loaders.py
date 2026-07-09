from pathlib import Path
from langchain_core.documents import Document
def load_documents(kb_path):
    documents = []
    for file in Path(kb_path).glob("*.md"):
        text = file.read_text(encoding="utf-8")
        documents.append(
            Document(page_content=text,metadata={"source_file": file.name}))
    return documents