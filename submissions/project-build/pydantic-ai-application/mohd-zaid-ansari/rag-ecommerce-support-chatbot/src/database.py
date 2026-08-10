from src.config import DATASET_PATH, VECTORE_STORE_PATH, EMBEDDING_MODEL,CHUNK_SIZE, CHUNK_OVERLAP, TOP_K
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import chromadb
import time
from chromadb.config import Settings
from langchain_chroma import Chroma

#================================================================================================================================

#loaders

from langchain_community.document_loaders import PyPDFDirectoryLoader
def load_pdf(DATSET_PATH=DATASET_PATH):
    loaders=PyPDFDirectoryLoader(DATSET_PATH)
    document=loaders.load()
    return document

#===============================================================================================================================

#chunking

from langchain_text_splitters import RecursiveCharacterTextSplitter
def create_chunks(document):
    text_splitter=RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name='cl100k_base',
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks=text_splitter.split_documents(document)
    return chunks

#==============================================================================================================================

#metadata

def get_metadata(chunks):
    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"]=f"chunk_{idx}"
        source_file=chunk.metadata.get("source", "")
        chunk.metadata["source_file"]=source_file

    return chunks

#==============================================================================================================================

#embedding

def get_embedding_model():
    embedding_model=embedding_model=HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL)
    return embedding_model

#===============================================================================================================================

#vector_database

collection_name='ebay_docs'
collection_path='chroma_db'

def create_vector_store(embedding_model):
    chroma_client=chromadb.PersistentClient(
        path=collection_path,
        settings=Settings(
               anonymized_telemetry=False
        )
    )

    vector_store= Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=collection_path,
        client=chroma_client,
        collection_metadata={
            'hnsw:space':"cosine"
        }
    )
    return vector_store

def index_chunk_to_vectorstore(
        chunks,
        vectorstore
):
    i=0
    while i<len(chunks):
        vectorstore.add_documents(
            documents=chunks[i:i+25],
            ids=[
                f"text_{j}"
                for j in range(
                    i,
                    min(i+25, len(chunks))
                )
            ]
        )
        print( f"Indexed {min(i+25,len(chunks))}/{len(chunks)}")
        i+=25
        time.sleep(5)
        print("index completed")

#=========================================================================================================================================
    
#retriver

def retrive_data(
        query:str,
        vectore_store,
        top_k: int=TOP_K
):
    result=vectore_store.similarity_search_with_score(
        query,
        k=top_k
    )

    retrived_chunks=[]
    for doc, score in result:
        retrived_chunks.append(
            {
            "source_file":
                doc.metadata.get("source_file"),

            "chunk_id":
                doc.metadata.get("chunk_id"),

            "content":
                doc.page_content,
            }
        )

        return retrived_chunks

