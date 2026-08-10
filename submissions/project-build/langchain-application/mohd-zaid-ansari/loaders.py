from langchain_community.document_loaders import PyPDFDirectoryloader

pdf_location='data/raw'

def load_pdf(pdf_location):
    loader=PyPDFDirectoryloader(pdf_location)
    documents=loader.load()
    return documents