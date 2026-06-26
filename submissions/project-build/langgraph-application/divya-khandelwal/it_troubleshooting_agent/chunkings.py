from functools import lru_cache
import os
import time

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from loaders import load_data

load_dotenv()


def chunking(documents):

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=int(os.getenv("CHUNK_SIZE", 900)),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 120)),
    )

    chunks = text_splitter.split_documents(documents)
    print("length of chunks: ", len(chunks))
    return chunks


def embedding():
    model_name = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-mpnet-base-v2",
    )
    return HuggingFaceEmbeddings(model_name=model_name)


def create_db():

    # Load PDF
    data = load_data()
    print("pdf loaded")

    # Create chunks
    chunks = chunking(data)
    print("chunks created")
    print("Total chunks:", len(chunks))


    # Create embeddings
    embeddings = embedding()
    print("embedding done")


    collection_name = "enterprise-policy-data"
    vector_store_path = os.getenv("VECTOR_STORE_PATH", "./vector_store")

    chromadb_client = chromadb.PersistentClient(
        path=vector_store_path
    )

    vectorstore_persistent = Chroma(
        collection_name=collection_name,
        collection_metadata={
            "hnsw:space": "cosine"
        },
        embedding_function=embeddings,
        client=chromadb_client,
        persist_directory=vector_store_path,
    )


    # Add documents in batches
    batch_size = 500

    for i in range(0, len(chunks), batch_size):

        batch_chunks = chunks[i:i + batch_size]

        ids = [
            "text_" + str(index)
            for index in range(i, i + len(batch_chunks))
        ]

        vectorstore_persistent.add_documents(
            documents=batch_chunks,
            ids=ids
        )

        print(
            f"Added chunks {i} to {i + len(batch_chunks)}"
        )

        time.sleep(2)


    print("Vector database created successfully")

    return vectorstore_persistent




if __name__ == "__main__":
    create_db()