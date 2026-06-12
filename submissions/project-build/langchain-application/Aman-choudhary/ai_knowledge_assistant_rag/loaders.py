import os
import re
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from config import Config

def load_pdf_documents():
    """
    Loads PDF documents from the directory specified in Config.
    Uses DirectoryLoader to find all PDFs and PyPDFLoader for parsing.
    """
    print(f"Attempting to load documents from: {Config.DATA_DIR}")
    
    loader = DirectoryLoader(str(Config.DATA_DIR), glob="**/*.pdf",loader_cls=PyPDFLoader,show_progress=True)
    docs = loader.load()
    for doc in docs:
        source_path = doc.metadata.get("source", "")
        file_name = os.path.basename(source_path)
        year_match = re.search(r'\b(20|19)\d{2}\b', file_name)
        doc.metadata["source_file"] = file_name
        doc.metadata["page_number"] = doc.metadata.get("page", 0) + 1
        doc.metadata["document_type"] = "PDF"
        doc.metadata["year"] = year_match.group(0) if year_match else "Unknown"
    return docs