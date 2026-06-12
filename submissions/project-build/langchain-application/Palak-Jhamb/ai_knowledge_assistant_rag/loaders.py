from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_documents(folder_path):

    documents = []
    pdf_files = Path(folder_path).glob("*.pdf")
    for pdf in pdf_files:
        loader = PyPDFLoader(str(pdf))
        docs = loader.load()

        documents.extend(docs)

    return documents