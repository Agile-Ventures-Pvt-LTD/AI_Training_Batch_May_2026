from langchain_community.document_loaders import PyPDFLoader


def pdf_loader():

    pdf_path = r"C:\Users\Divya Khandelwal\Desktop\ai_knowledge_assistent_rag\data\raw\Amazon-2025-Annual-Report.pdf"

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    print("Number of pages loaded:", len(documents))

    return documents