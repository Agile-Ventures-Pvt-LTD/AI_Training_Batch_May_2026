
import chromadb

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chunking import split_documents

chunks=split_documents()


# def create_vector_db(chunks):

client = chromadb.PersistentClient(
    path="data/vector_store"
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    client=client
)

    # return vectordb