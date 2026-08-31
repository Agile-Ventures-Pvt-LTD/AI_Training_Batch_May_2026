from pathlib import Path
import re
import os
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma,FAISS
from langchain_core.documents import Document
from typing import List
import logging
from config import LOGISTICS_KB_PATH, EMBEDDING_MODEL


CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
BASE_DIR = Path(__file__).resolve().parent
VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH', str(BASE_DIR / 'chroma_db'))
DATA_PATH = os.getenv('DATA_PATH', str(BASE_DIR / 'data'))
SUPPORTED_FILES = ".txt"

def load_documents(folder_path: str) -> List[Document]:
    documents = []
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"{folder_path} does not exist")
        
    for file in folder.iterdir():
        if file.suffix.lower() not in SUPPORTED_FILES:
            continue
        try:
            if file.suffix == ".txt":
                loader = TextLoader(str(file))
            docs = loader.load()
            for doc in docs:
                doc.metadata["source_file"] = file.name
                doc.page_content = doc.page_content
            documents.extend(docs)
        except Exception as e:
            print(f"Failed loading {file}: {e}")
    return documents

def chunk_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    processed_chunks = []
    for idx, chunk in enumerate(chunks):
        metadata = chunk.metadata.copy()
        metadata["chunk_id"] = f"chunk_{idx:05d}"
        metadata["text"] = chunk.page_content
        chunk.metadata = metadata
        processed_chunks.append(chunk)
    return processed_chunks

def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def create_vector_store(chunks: List[Document]) -> Chroma:
    embeddings = get_embedding_model()
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH
    )
    return vector_store

def load_vector_store() -> Chroma:
    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError(f"Vector Store directory not found at {VECTOR_STORE_PATH}")
    embeddings = get_embedding_model()
    return Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )

def build_index():
    docs = load_documents(DATA_PATH)
    if not docs:
        raise ValueError(f"No documents found to parse or index inside: {DATA_PATH}")
    chunks = chunk_documents(docs)
    create_vector_store(chunks)
    print("Vector Store Built Successfully.")

if __name__ == "__main__":
    build_index()

logger = logging.getLogger(__name__)

class RAG_Retrieve:
    def __init__(self,Knowledge_Base_Path:Path=LOGISTICS_KB_PATH,Embedding_model:Path=EMBEDDING_MODEL,chunk_size:int=250,chunk_overlap:int=100):
        self.Knowledge_Base_Path = Knowledge_Base_Path
        self.Embedding_model = Embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def embedding(self):
        if self.embedding is None:
            self.embedding= HuggingFaceEmbeddings(model_name= self.Embedding_model)
        return self.embedding
    
    def build_vector_store(self,chunks):
        embeddings = self._get_embeddings()
        return FAISS.from_documents(chunks, embeddings)

    def build(self):
        logger.info("Building RAG pipeline from %s", self.knowledge_base_path)
        documents = self._load_documents()
        chunks = self._split_documents(documents)
        logger.info("Split document into %d chunks", len(chunks))
        vector_store = self._build_vector_store(chunks)
        self._retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},
        )
        logger.info("RAG pipeline built successfully")
        return self

    def retrieve(self, query: str, k: int = 5) -> list[str]:
        if self._retriever is None:
            self.build()

        docs = self._retriever.invoke(query)
        rules = [doc.page_content.strip() for doc in docs]
        logger.info("Retrieved %d rules for query", len(rules))
        return rules

    def retrieve_context(self, query: str, k: int = 5) -> str:
        rules = self.retrieve(query, k)
        return "\n\n".join(rules)
    