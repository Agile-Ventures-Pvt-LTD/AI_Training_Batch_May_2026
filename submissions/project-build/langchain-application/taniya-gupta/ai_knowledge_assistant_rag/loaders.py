import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader

def load_documents(directory):
    documents=[]
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            loader=PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith(".txt"):
            loader=TextLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith(".md"):
            loader=UnstructuredMarkdownLoader(file_path)
            documents.extend(loader.load())
    return documents