from pathlib import Path
from langchain_community.document_loaders import UnstructuredMarkdownLoader

#I am using Unstructured Markdown loader from langchain community 

from config import POLICY_DATA_PATH, POLICY_DOMAIN_MAP


def load_policy_documents(data_dir: str = None) -> list:
    data_dir = data_dir or POLICY_DATA_PATH

    docs = []
    for f in Path(data_dir).iterdir():

        loader = UnstructuredMarkdownLoader(str(f), mode="single")
        loaded = loader.load()  

        policy_domain = POLICY_DOMAIN_MAP.get(f.stem.lower(), "OTHER")
        for doc in loaded:
            doc.metadata["source_file"] = f.name
            doc.metadata["policy_domain"] = policy_domain

        docs.extend(loaded)

    print(f"Loaded {len(docs)} documents")
    return docs