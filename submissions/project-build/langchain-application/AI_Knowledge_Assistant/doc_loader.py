from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path

def load_documents(data_dir: str = "data/raw") -> list:
    docs = []
    for f in Path(data_dir).iterdir():
        if f.suffix.lower() == ".pdf":
            loader = PyMuPDFLoader(str(f))
            loaded = loader.load()
            docs.extend(loaded)
    print(f"Loaded {len(docs)} pages")
    return docs