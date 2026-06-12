from langchain_chroma import Chroma
from chunking import chunks
from embedding import embeddings


import shutil
import os

if os.path.exists("vector_db"):
    shutil.rmtree("vector_db")


vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vector_db"
)

