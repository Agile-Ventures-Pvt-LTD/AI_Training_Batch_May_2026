from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from langchain_community.embeddings import (
    SentenceTransformerEmbeddings
)

from loaders import load_documents

from config import (
    KB_PATH,
    VECTOR_STORE_PATH,
    EMBEDDING_MODEL,
    TOP_K
)

embeddings = SentenceTransformerEmbeddings(
    model_name=EMBEDDING_MODEL
)


def build_vector_store():

    docs = load_documents(KB_PATH)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120
    )

    chunks = splitter.split_documents(
        docs
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH
    )

    return db


def get_retriever():

    db = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )

    return db.as_retriever(
        search_kwargs={
            "k": TOP_K
        }
    )