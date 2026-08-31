import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf_documents(data_folder: str):
   # Load all PDF files from data/raw directory.

    documents = []

    if not os.path.exists(data_folder):
        raise FileNotFoundError(
            f"Folder not found: {data_folder}"
        )

    pdf_files = [
        file
        for file in os.listdir(data_folder)
        if file.lower().endswith(".pdf")
    ]

    if not pdf_files:
        raise ValueError("No PDF files found in data/raw")

    for pdf_file in pdf_files:

        pdf_path = os.path.join(
            data_folder,
            pdf_file
        )

        loader = PyPDFLoader(pdf_path)

        pages = loader.load()

        for page in pages:

            metadata = page.metadata.copy()

            metadata["source_file"] = pdf_file

            metadata["page_number"] = metadata.get("page",0) + 1

            metadata["document_type"] = ("annual_report")

            documents.append(
                Document(
                    page_content=page.page_content,
                    metadata=metadata
                )
            )

    return documents