from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP,DB_PATH
from config import EMBEDDING_MODEL
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader


#load pdf from path
def load_documents(FOLDER_PATH):

    documents = []    
    loader = PyMuPDF4LLMLoader(FOLDER_PATH ) 
    docs = loader.lazy_load()
    # doc = pymupdf.open(FOLDER_PATH)
    # for page in doc:
    documents.extend(docs)
        
    return documents

    
# split data using recursive text splitter
def split_documents(documents):
    # splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=CHUNK_SIZE,
    #     chunk_overlap=CHUNK_OVERLAP,
    # )
    # return splitter.split_documents(documents)r

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)
    return texts


#get embedding model from ugging face
def get_embedding_model():
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings


import time
import chromadb
from langchain_chroma import Chroma

def create_vector_store(FOLDER_PATH):
    documents = load_documents(FOLDER_PATH)
    
    chunks= split_documents(documents)
    embedding_model = get_embedding_model()

    chromadb_client = chromadb.PersistentClient(path=DB_PATH)
    print("Database Created at:", DB_PATH)

    print(len(documents))
    vectorstore = Chroma(
    collection_name="seller_guide_collection",
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding_model,
    client=chromadb_client,
    persist_directory=DB_PATH
    )
    print("Vector Store Created")
    print("Adding documents to the vector store")
    print(chromadb_client.count_collections())
    i = 0
    print("total chunks",len(chunks))
    while i < len(chunks):
        vectorstore.add_documents( 
            documents=chunks[i:i+10], 
            ids=["text_" + str(i) for i in range(i, i+10)],
        )
    
        i += 10
        print(f"Added {i} / {len(chunks)} chunks to the vector store")
        time.sleep(1)

    return vectorstore



