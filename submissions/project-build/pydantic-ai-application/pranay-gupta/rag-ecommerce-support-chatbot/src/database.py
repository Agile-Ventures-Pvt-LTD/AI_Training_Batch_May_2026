from langchain_community.vectorstores import Chroma

from config import TOP_K,EMBEDDING_MODEL,CHUNK_OVERLAP,CHUNK_SIZE,VECTOR_STORE_PATH

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
# import chromadb

def load_pdf_document():
    pdf_folder_location = "data"
    pdf_loader = PyPDFLoader(pdf_folder_location)
    return pdf_loader

def chunk_document():
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )
    pdf = load_pdf_document()
    processed_docs = []
    chunk_counter = 1
    for document in pdf:

        chunks = text_splitter.split_text(document.page_content)

        for chunk in chunks:
            metadata = document.metadata.copy()
            metadata["chunk_id"] = (
                f"chunk_{chunk_counter:05d}"
            )
            processed_docs.append(
                {
                    "text": chunk,
                    "metadata": metadata
                }
            )

            chunk_counter += 1

    return processed_docs

def embedding_model():
    embeddings =  HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    return embeddings


def create_documents():
    
    docs = []
    chunk_data = chunk_document()
    for chunk in chunk_data:
        docs.append(
            Document(
                page_content=chunk["text"],
                metadata=chunk["metadata"]
            )
        )
    return docs


def build_vector_store():
    embeddings = embedding_model()
    documents = create_documents()

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH
    )
    print(
        f"Vector store created with "
        f"{len(documents)} chunks."
    )

    return vector_store


def load_vector_store():
    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError(
            "Vector database not found."
        )
    embeddings = embedding_model()

    vector_store = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )
    return vector_store

def get_retriever():
    vector_store = build_vector_store()
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K
        }
    )

def retrieve_documents(question):
    retriever = get_retriever()
    docs = retriever.invoke(question)

    return docs