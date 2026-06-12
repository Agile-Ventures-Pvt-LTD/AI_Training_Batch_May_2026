
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    try:
        return PyPDFLoader(file_path).load()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return []
