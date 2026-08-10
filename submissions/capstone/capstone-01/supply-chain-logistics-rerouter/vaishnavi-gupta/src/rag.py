from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import FAISS


def load_documents():

    documents = []

    data_folder = "data/  .txt"

    for file in data_folder.rglob("*"):

        suffix = file.suffix.lower()

        if suffix == ".pdf":

            loader = PyPDFLoader(str(file))

        elif suffix == ".txt":

            loader = TextLoader(str(file))

        elif suffix == ".md":

            loader = UnstructuredMarkdownLoader(str(file))

        else:
            continue

        docs = loader.load()

        for doc in docs:

            doc.metadata["source_file"] = file.name

            documents.append(doc)

    return documents


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=100,

        chunk_overlap=10

    )

    chunks = splitter.split_documents(documents)

    return chunks


def get_embeddings():

    embedding_model = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2"

    )

    return embedding_model


def create_vector_store(chunks):

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory="vectordb/faiss.db"

    )

    return vector_store


def get_retriever(vector_store):

    retriever = vector_store.as_retriever(

        search_kwargs={

            "k": 4

        }

    )

    return retriever