from langchain_chroma import Chroma
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

from embeddings import embedding_model
from loaders import load_pdf_file
from chunking import chunk_documents


COLLECTION_NAME = "tesla-Amazon_2025"
PERSIST_DIRECTORY = "./data/vector_store"
RAW_PDF_PATH = "./data/raw/Amazon-2025-Annual-Report.pdf"


def get_vectorstore(embeddings=None):
    if embeddings is None:
        embeddings = embedding_model()

    chromadb_client = chromadb.PersistentClient(
        path=PERSIST_DIRECTORY
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        collection_metadata={"hnsw:space": "cosine"},
        embedding_function=embeddings,
        client=chromadb_client,
        persist_directory=PERSIST_DIRECTORY,
    )

    return vectorstore


def create_vectorstore(chunks, embeddings):
    vectorstore = get_vectorstore(embeddings)

    # Add documents with metadata such as "chunk_id", "source_file", "page_number".
    i = 0
    while i < len(chunks):
        batch = chunks[i:i + 500]
        vectorstore.add_documents(
            documents=batch,
            ids=["text_" + str(doc_id) for doc_id in range(i, i + len(batch))],
        )

        i += 500

    return vectorstore


def build_vectorstore(pdf_path=RAW_PDF_PATH):
    chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "150"))

    documents = load_pdf_file(pdf_path)
    chunks = chunk_documents(documents, chunk_size, chunk_overlap)
    embeddings = embedding_model()

    return create_vectorstore(chunks, embeddings)


vectorstore = None


def load_vectorstore():
    global vectorstore

    if vectorstore is None:
        vectorstore = get_vectorstore()

    return vectorstore

if __name__ == "__main__":
    build_vectorstore()
