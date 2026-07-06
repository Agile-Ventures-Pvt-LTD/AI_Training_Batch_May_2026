import os
from langchain_community.document_loaders import TextLoader
from pathlib import Path

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
load_dotenv()

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 100))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP",50))

VECTOR_DB = os.getenv("VECTOR_DB", "chroma")
TOP_K = int(os.getenv("TOP_K", 3))

CHROMA_DB_PATH = Path("chroma_db")

embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def load_data(db_path="data/logistics_knowledge_base.txt"):
    documents = []
    for fname in os.listdir(db_path):
        fpath = os.path.join(db_path, fname)
        if fname.endswith(".txt"):
            try:
                loader = TextLoader(fpath, encoding="utf-8")
                loader.load()
            
            except Exception as e:
               print(f"Error loading {fname}: {e}")
    print("loaded")           

    return documents

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    return chunks

def create_vectorstore():

    documents = load_pdf()

    chunks = split_documents(documents)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DB_PATH),
        collection_name="logistic_rule"
    )

    print("ChromaDB created successfully.")

    return vectorstore

def load_vectorstore():

    print("Loading existing ChromaDB...")

    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=embedding_model,
        collection_name="seller_guide"
    )

    return vectorstore

def get_vectorstore():

    if not CHROMA_DB_PATH.exists():

        print("ChromaDB not found.")
        print("Creating vector database...")

        return create_vectorstore()

    return load_vectorstore()


def get_retriever():

    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K
        }
    )

    return retriever
