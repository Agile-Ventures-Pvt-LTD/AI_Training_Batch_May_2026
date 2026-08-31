from pathlib import Path
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from config import KB_PATH


def load_kb_documents():
    if not KB_PATH or not Path(KB_PATH).exists():
        raise FileNotFoundError(f"Knowledge base path not found: {KB_PATH}")
    loader = DirectoryLoader(KB_PATH,
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()

    for doc in documents:
        source_name = Path(doc.metadata["source"]).name
        doc.metadata["source_file"] = source_name
        doc.metadata["issue_domain"] = extract_issue_domain(source_name)
    return documents


def extract_issue_domain(filename: str) -> str:
    "Examples: vpn_troubleshooting_guide.md -> VPN"
    mapping = {
        "vpn": "VPN",
        "email": "OUTLOOK_EMAIL",
        "laptop": "LAPTOP_PERFORMANCE",
        "password": "PASSWORD_RESET",
        "network": "NETWORK_CONNECTIVITY",
        "printer": "PRINTER",
    }
    for key, domain in mapping.items():
        if key in filename.lower():
            return domain
    
    return "UNKNOWN"

