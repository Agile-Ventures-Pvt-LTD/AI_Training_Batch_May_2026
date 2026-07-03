import pymupdf
import asyncio
from pydantic_ai.embeddings.sentence_transformers import (
    SentenceTransformerEmbeddingModel,
)
from sentence_transformers import SentenceTransformer

# from langchain_chroma import Chroma
import time

import chromadb
from chromadb.utils import embedding_functions

# from models.schemas import RetrievedChunk

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME ="seller-guide-collect"

import chromadb

CHUNK_SIZE=900
CHUNK_OVERLAP=120
file_path="./data/directory/seller_guide.pdf"

#----------------------------loader-------------------------------

def loader():
    documents=[]

    text = ""

    doc = pymupdf.open(file_path)
    for page in doc:
        # print(page.get_text())
        extracted= page.get_text()

        if extracted:
            text += extracted + "\n"

            documents.append(
                {
                    "page_content": extracted
                }
            )
    return documents

documents=loader()
# print(documents)


#----------------------splitter--------------------------------



documents = loader()

def splitter():

    chunks = []

    for document in documents:

        text = document['page_content']

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk = text[start:end]

            chunks.append(chunk)

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks

chunks = splitter()
# print(chunks[0])

#---------------------------embedder-------------------------------



embeddings = SentenceTransformerEmbeddingModel('sentence-transformers/all-MiniLM-L6-v2')

def vectordb():


    # Initialize ChromaDB client with persistence
    client = chromadb.PersistentClient(path="chroma_db")

    # Configure sentence transformer embeddings
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )


    collection = client.get_or_create_collection(
        name="documents_collection",
        embedding_function=sentence_transformer_ef
    )

vectordb()

def process_document():
    """Process a single document and prepare it for ChromaDB"""
    try:

        file_name = os.path.basename()
        metadatas = [{"source": file_name, "chunk": i} for i in range(len(chunks))]
        ids = [f"{file_name}_chunk_{i}" for i in range(len(chunks))]

        return ids, chunks, metadatas
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return [], [], []


 


#---------------------------retriever-------------------------------------





class Retriever:

    def __init__(self):

        self.embedder = EmbeddingModel()
        self.vectordb = VectorDB()

    async def search(
        self,
        query: str,
        top_k: int = TOP_K,
    ) -> list[RetrievedChunk]:

        query_embedding = await self.embedder.embed_query(query)

        results = self.vectordb.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        retrieved = []

        for doc, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):

            retrieved.append(
                RetrievedChunk(
                    document=metadata["filename"],
                    content=doc,
                    score=distance,
                )
            )

        return retrieve