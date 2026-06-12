#Loading

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/raw/Amazon-2025-Annual-Report.pdf")

documents = loader.load()

