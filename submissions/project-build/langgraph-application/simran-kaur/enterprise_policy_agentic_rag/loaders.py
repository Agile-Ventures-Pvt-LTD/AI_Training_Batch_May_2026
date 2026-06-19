
# from pathlib import Path
# from langchain_community.document_loaders import TextLoader
# def load_markdown_directory():

#     documents = []

#     for md_file in Path(directory).glob("*.md"):
#         loader = TextLoader(str(md_file), encoding="utf-8")
#         documents.extend(loader.load())

#     return documents

directory="data/policies"


from pathlib import Path
from langchain_community.document_loaders import TextLoader


def load_documents():

    documents = []

    md_files = [
        "data/policies/ai_usage_policy.md",
        "data/policies/hr_leave_policy.md",
        "data/policies/it_security_policy.md",
        "data/policies/reimbursement_policy.md",
        "data/policies/travel_policy.md"
    ]

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
                "policy_domain": policy_name,
                "page_number": ""
            }

        documents.extend(docs)

    return documents

