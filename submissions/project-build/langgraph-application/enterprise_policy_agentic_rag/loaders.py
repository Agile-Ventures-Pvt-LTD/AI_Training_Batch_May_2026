import os
from typing import List, Dict
from langchain_community.document_loaders import TextLoader

POLICY_MAP = {
    "hr": "HR_LEAVE",
    "travel": "TRAVEL",
    "reimbursement": "REIMBURSEMENT",
    "it_security": "IT_SECURITY",
    "ai_usage": "AI_USAGE"
}

def load_documents(data_path: str) -> List[Dict]:
    docs = []

    for file in os.listdir(data_path):
        path = os.path.join(data_path, file)

        if file.endswith(".md") or file.endswith(".txt"):
            loader = TextLoader(path, encoding="utf-8")
            loaded_docs = loader.load()

            domain = file.replace("_policy.md", "").replace(".md", "")

            for d in loaded_docs:
                docs.append({
                    "text": d.page_content,
                    "source_file": file,
                    "policy_domain": POLICY_MAP.get(domain, "OTHER")
                })

    return docs