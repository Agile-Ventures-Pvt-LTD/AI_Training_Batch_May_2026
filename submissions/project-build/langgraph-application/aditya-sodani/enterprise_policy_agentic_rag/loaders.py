from pathlib import Path
from langchain_community.document_loaders import (TextLoader,PyPDFLoader)
from config import (POLICY_MAPPING,SUPPORTED_EXTENSIONS)
def load_single_file(file_path):
    """
    Load a single file and return documents.
    """
    suffix = file_path.suffix.lower()
    if suffix in [".md", ".txt"]:
        loader = TextLoader(str(file_path),encoding="utf-8")
        return loader.load()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
        return loader.load()
    return []
def load_documents(policy_data_path):
    """
    Load all policy files from data/policies.

    Returns:
        List[Document]
    """
    root = Path(policy_data_path)
    if not root.exists():
        raise FileNotFoundError(f"Policy folder not found: {policy_data_path}")
    documents = []
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        if (file_path.suffix.lower() not in SUPPORTED_EXTENSIONS):
            continue
        try:
            loaded_docs = load_single_file(file_path)
            policy_domain = POLICY_MAPPING.get(file_path.stem,"OTHER")
            for page_num, doc in enumerate(loaded_docs,start=1):
                doc.metadata.update({"source_file": file_path.name,"policy_domain": policy_domain,"page_number": page_num})
                documents.append(doc)
        except Exception as exc:
            print(f"[WARNING] Could not load "f"{file_path.name}: {exc}")
    return documents
def validate_documents(documents):
    """
    Remove empty documents.
    """
    cleaned_docs = []
    for doc in documents:
        content = (doc.page_content.strip()
            if doc.page_content
            else "")
        if not content:
            continue
        cleaned_docs.append(doc)
    return cleaned_docs
def print_document_summary(documents):
    """
    Debug helper.
    """
    print("\nLoaded Documents Summary")
    print("-" * 40)
    print(f"Total Documents: "f"{len(documents)}")
    domains = {}
    for doc in documents:
        domain = doc.metadata.get("policy_domain","UNKNOWN")
        domains[domain] = (domains.get(domain, 0) + 1)
    for domain, count in domains.items():
        print(f"{domain}: {count}")
if __name__ == "__main__":
    from config import POLICY_DATA_PATH
    docs = load_documents(POLICY_DATA_PATH)
    docs = validate_documents(docs)
    print_document_summary(docs)
    if docs:
        print("\nSample Metadata:")
        print(docs[0].metadata)
        print("\nSample Content:")
        print(docs[0].page_content[:300])