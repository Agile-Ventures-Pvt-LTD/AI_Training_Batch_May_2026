from pathlib import Path
from langchain_core.documents import Document
from config import KB_PATH


def get_issue_domain(filename: str) -> str:
    """
    Converting filename into issue type.
    """

    filename = filename.lower()

    if "vpn" in filename:
        return "VPN"

    if "email" in filename or "outlook" in filename:
        return "OUTLOOK_EMAIL"

    if "laptop" in filename:
        return "LAPTOP_PERFORMANCE"

    if "password" in filename:
        return "PASSWORD_RESET"

    if "network" in filename:
        return "NETWORK_CONNECTIVITY"

    if "printer" in filename:
        return "PRINTER"

    return "UNKNOWN"


def load_knowledge_base():
    documents = []

    kb_folder = Path(KB_PATH)

    markdown_files = kb_folder.glob("*.md")

    for file_path in markdown_files:

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        document = Document(
            page_content=content,
            metadata={
                "source_file": file_path.name,
                "issue_domain": get_issue_domain(file_path.name),
                "chunk_id": "raw_document"
            }
        )
        documents.append(document)

    return documents