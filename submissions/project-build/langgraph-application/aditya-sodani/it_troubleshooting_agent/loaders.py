import os
from langchain_community.document_loaders import TextLoader

def load_kb_documents(kb_path):
    docs = []

    for file in os.listdir(kb_path):
        if file.endswith(".md") or file.endswith(".txt"):
            path = os.path.join(kb_path, file)
            loader = TextLoader(path)
            loaded = loader.load()

            for i, d in enumerate(loaded):
                d.metadata["source_file"] = file
                d.metadata["chunk_id"] = f"{file}_chunk_{i}"
                docs.append(d)

    return docs