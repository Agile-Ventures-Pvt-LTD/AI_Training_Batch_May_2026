import re
from langchain_community.document_loaders import PyPDFDirectoryLoader

pdf_folder_location = "data/raw"
pdf_loader = PyPDFDirectoryLoader(pdf_folder_location)

def clean_text(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text)
    
    return text

def preprocess_documents(docs):
    cleaned_docs = []
    for doc in docs:
        cleaned_text = clean_text(doc.page_content)
        
        cleaned_docs.append({
            "text": cleaned_text,
            "source": doc.metadata.get("source", ""),
            "page": doc.metadata.get("page", None)
        })
    return cleaned_docs

docs = pdf_loader.load()
preprocessed_docs = preprocess_documents(docs)
