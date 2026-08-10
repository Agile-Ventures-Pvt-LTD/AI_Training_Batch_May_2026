import os
from langchain_community.document_loaders import TextLoader

def load_documents(KB_path="data/knowledge_base"):
    documents = []
    for fname in os.listdir(KB_path):
        fpath = os.path.join(KB_path, fname)
        if fname.endswith((".md", ".txt", ".pdf")):
            try:
                loader = TextLoader(fpath, encoding="utf-8")
                docs = loader.load()
                for d in docs:
                    d.metadata["source_file"] = fname
                    domain = fname.replace("_KB_path.md", "").replace("_KB_path.txt", "").replace(".md", "").replace(".txt", "").upper()
                    d.metadata["KB_domain"] = domain
                documents.extend(docs)
            except Exception as e:
                print(f"Error loading {fname}: {e}")
    return documents
