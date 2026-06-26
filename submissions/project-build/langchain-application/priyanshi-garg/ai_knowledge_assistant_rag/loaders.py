from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

RAW_FOLDER = Path("data/raw/Amazon-2025-Annual-Report.pdf")

load_documents = PyPDFLoader(RAW_FOLDER)