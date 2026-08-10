
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
import uuid
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


def txt_loader(txt_directory):

    documents = []

    txt_files = list(Path(txt_directory).glob("**/*.txt"))

    print(f"Found {len(txt_files)} PDF files")

    for txt in txt_files:

        loader = TextLoader(str(txt))

        docs = loader.load()

        for doc in docs:
            doc.metadata["source_file"] = txt.name

        documents.extend(docs)

    print(f"Loaded {len(documents)} pages")

    return documents



documents = txt_loader("data")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = FAISS.from_documents(documents, embedding=embedding_model)


def retriever(query1):

    docs1 = vector_store.similarity_search(query1, k=2)
    dict={} # Get top 2 results
    for i, doc in enumerate(docs1):
        # print(f"  Result {i+1}: {doc.page_content}")
        dict[f"{i+1}"] = doc.page_content

    return dict

print(retriever("warehouse has an ELEVATED"))