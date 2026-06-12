from langchain_community.document_loaders import PyPDFLoader

def load_pdf_file(file_path):

    loader=PyPDFLoader(file_path)
    documents=loader.load()
    return documents