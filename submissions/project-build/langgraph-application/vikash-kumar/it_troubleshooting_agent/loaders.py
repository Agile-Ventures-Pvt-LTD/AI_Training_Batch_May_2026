from pathlib import Path

from langchain_community.document_loaders import TextLoader

ISSUE_CLASSIFICATION = {"vpn_troubleshooting_guide": "VPN","email_outlook_troubleshooting_guide": "OUTLOOK_EMAIL","laptop_performance_guide": "LAPTOP_PERFORMANCE","password_reset_guide": "PASSWORD_RESET","network_connectivity_guide": "NETWORK_CONNECTIVITY",}

def get_issue_classification(file_name: str):
    """THis will classify the issue"""
    path1 = Path(file_name).stem
    return ISSUE_CLASSIFICATION.get(path1,"OTHER")

def load_documents(policy_path):
    """THis will load the documents"""
    documents = []
    policy_dir = Path(policy_path)

    for file_path in policy_dir.iterdir():
        if file_path.suffix in [".md"]:
            docs = TextLoader(str(file_path),encoding="utf-8").load()
        else:
            continue
        domain = get_issue_classification(file_path.name)
        for doc in docs:
            doc.metadata["source_file"] = file_path.name
            doc.metadata["policy_domain"] = domain
            documents.append(doc)
    return documents