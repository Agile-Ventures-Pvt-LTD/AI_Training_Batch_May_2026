import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document
from config import config

class Documentloader:
    def __init__(self,path=config.DATA_PATH):
        self.path=path

    def load(self):
        documents=[]
        for filename in os.listdir(self.path):
            f_path=os.path.join(self.path, filename)
            domain=filename.replace("_policy.md","").upper()
            if filename.endswith(".md"):
                loader=TextLoader(f_path,encoding='utf-8')
                docs=loader.load()
            elif filename.endswith(".pdf"):
                loader=PyPDFLoader(f_path)
                docs=loader.load()
            elif filename.endswith(".txt"):
                loader=TextLoader(f_path, encoding='utf-8')
                docs=loader.load()
            else:
                continue
            for doc in docs:
                doc.metadata["source_file"]=filename
                doc.metadata["policy_domain"]=domain
            documents.extend(docs)
        return documents
    