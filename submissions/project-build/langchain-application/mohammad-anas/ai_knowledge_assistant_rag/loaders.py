import os
import re
from langchain_community.document_loaders import PyMuPDFLoader
from config import Config

def cleaning_txt(txt: str) -> str:
    """remove the empty lines and white spaces"""
    txt = re.sub(r"\n\s*\n","\n", txt)
    return re.sub(r'[ \t]+', ' ', txt).strip()

def load_docs():
    """load the pdf from the data folder"""
    docs = []
    try:
        # Loop through the directory to get actual file paths
        for filename in os.listdir(Config.RAW_DATA_DIR):
            if filename.endswith(".pdf"):
                filepath = os.path.join(Config.RAW_DATA_DIR, filename)
                loader = PyMuPDFLoader(filepath)
                pages = loader.load()
                for idx, page in enumerate(pages):
                    cleaned = cleaning_txt(page.page_content)
                    if cleaned:
                        page.page_content = cleaned
                        page.metadata.update({
                            "source_file": filename,
                            "page_number": idx + 1
                        })
                        docs.append(page)
    except Exception as e:
        print(f"cannot load pdf: {e}")
    return docs