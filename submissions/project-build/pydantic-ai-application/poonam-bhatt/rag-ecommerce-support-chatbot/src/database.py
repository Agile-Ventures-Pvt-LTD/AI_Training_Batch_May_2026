
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "Advanced_Business_Seller_Guide_May09.pdf"

VECTOR_DB_PATH = BASE_DIR

MODEL_NAME = "all-MiniLM-L6-v2"


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#Document Loader

from pathlib import Path
from langchain_chroma import Chroma

from langchain_community.document_loaders import TextLoader


def load_documents(path):

    docs = []

    for file in Path(path).glob("*.md"):

        loader = TextLoader(str(file))

        docs.extend(loader.load())

    return docs


from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=100,

    )

    return splitter.split_documents(documents)


from langchain.embeddings import HuggingFaceEmbeddings

from config import MODEL_NAME


def get_embeddings():

    return HuggingFaceEmbeddings(

        model_name=MODEL_NAME

    )



from rag.embeddings import get_embeddings


def create_vector_db(chunks):

    embeddings = get_embeddings()

    db = Chroma.from_documents(

        chunks,

        embeddings,
        persist_directory=VECTOR_DB_PATH

    )

    return db


def retrieve(db, query):

    return db.similarity_search(

        query,

        k=3

    )










# Project: P005 RAG Ecommerce support chatbot
# Author: Poonam Bhatt