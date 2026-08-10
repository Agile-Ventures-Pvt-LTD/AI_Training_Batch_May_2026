from pathlib import Path
from langchain_community.document_loaders import TextLoader


def load_documents():

    documents = []

    md_files = ["data/knowledge_base/email_outlook_troubleshooting_guide.md",
                "data/knowledge_base/laptop_performance_guide.md",
                "data/knowledge_base/network_connectivity_guide.md",
                "data/knowledge_base/password_reset_guide.md",
                "data/knowledge_base/printer_troubleshooting_guide.md",
                "data/knowledge_base/vpn_troubleshooting_guide.md"]

    for file_path in md_files:

        loader = TextLoader(
            file_path=file_path,
            encoding="utf-8"
        )

        docs = loader.load()

        policy_name = Path(file_path).stem

        for doc in docs:
            doc.metadata = {
                "source_file": Path(file_path).name,
                "issue_domain": policy_name,
                "page_number": ""
            }

        documents.extend(docs)

        return documents