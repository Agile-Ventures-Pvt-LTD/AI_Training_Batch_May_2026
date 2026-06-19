from pathlib import Path

from langchain_community.document_loaders import TextLoader

POLICY_CATEGORY= {"hr_leave_policy": "HR_LEAVE","travel_policy": "TRAVEL","reimbursement_policy": "REIMBURSEMENT","it_security_policy": "IT_SECURITY","ai_usage_policy": "AI_USAGE",}

def get_policy_domain(file_name: str):
    """THis will classify the policy domain"""
    path1 = Path(file_name).stem
    return POLICY_CATEGORY.get(path1,"OTHER")

def load_documents(policy_path):
    """THis will load the documents"""
    documents = []
    policy_dir = Path(policy_path)

    for file_path in policy_dir.iterdir():
        if file_path.suffix in [".md"]:
            docs = TextLoader(str(file_path),encoding="utf-8").load()
        else:
            continue
        domain = get_policy_domain(file_path.name)
        for doc in docs:
            doc.metadata["source_file"] = file_path.name
            doc.metadata["policy_domain"] = domain
            documents.append(doc)
    return documents