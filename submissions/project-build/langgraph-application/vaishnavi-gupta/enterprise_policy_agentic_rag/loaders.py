from langchain_community.document_loaders import PyPDFDirectoryLoader


loader = PyPDFDirectoryLoader(
    "enetrprise_policy_agentic_rag_dataset1",
    glob="*.pdf"
)

pdf_loader = PyPDFDirectoryLoader(pdf_folder_location)


pdf_folder_location = "enetrprise_policy_agentic_rag_dataset1"

