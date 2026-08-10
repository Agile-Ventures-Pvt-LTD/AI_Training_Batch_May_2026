from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os



def get_retriever(vectorstore):

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    return retriever
