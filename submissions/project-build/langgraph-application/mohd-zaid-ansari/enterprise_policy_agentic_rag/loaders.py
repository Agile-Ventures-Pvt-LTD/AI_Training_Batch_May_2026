from langchain_community.document_loaders import PyPDFDirectoryLoader
from config import POLICY_DATA_PATH

def load_pdf(POLICY_DATA_PATH=POLICY_DATA_PATH):
    loader=PyPDFDirectoryLoader(POLICY_DATA_PATH)
    documents=loader.load()
    return documents

# from langchain_community.document_loaders import DirectoryLoader
# from langchain_community.document_loaders import UnstructuredMarkdownLoader 
# from config import POLICY_DATA_PATH

# def load_documents(POLICY_DATA_PATH=POLICY_DATA_PATH):
#     loader = DirectoryLoader(
#         POLICY_DATA_PATH, 
#         glob="**/*.md", 
#         loader_cls=UnstructuredMarkdownLoader,
#         show_progress=True,
#         use_multithreading=True
#     )
#     documents = loader.load()
#     return documents
