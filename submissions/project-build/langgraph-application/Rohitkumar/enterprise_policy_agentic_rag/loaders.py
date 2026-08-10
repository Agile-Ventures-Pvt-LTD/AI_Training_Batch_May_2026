import os
from langchain_community.document_loaders import TextLoader

def load_policy_documents(policy_path="data/policies"):
    documents = []
    for fname in os.listdir(policy_path):
        fpath = os.path.join(policy_path, fname)
        if fname.endswith((".md", ".txt", ".pdf")):
            try:
                loader = TextLoader(fpath, encoding="utf-8")
                docs = loader.load()
                for d in docs:
                    d.metadata["source_file"] = fname
                    domain = fname.replace("_policy.md", "").replace("_policy.txt", "").replace(".md", "").replace(".txt", "").upper()
                    d.metadata["policy_domain"] = domain
                documents.extend(docs)
            except Exception as e:
                print(f"Error loading {fname}: {e}")
    return documents