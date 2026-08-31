import os
import re
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
BASE_DIR = Path(__file__).resolve().parent
VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH', str(BASE_DIR / 'chroma_db'))
DATA_PATH = os.getenv('DATA_PATH', str(BASE_DIR / 'data'))
SUPPORTED_FILES = ".pdf"

def load_documents(folder_path: str) -> List[Document]:
    documents = []
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"{folder_path} does not exist")
        
    for file in folder.iterdir():
        if file.suffix.lower() not in SUPPORTED_FILES:
            continue
        try:
            if file.suffix == ".pdf":
                loader = PyPDFLoader(str(file))
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

# For Database connection to our Agent
from pydantic_ai import Agent
from database_pydantic_ai import (
    SQLiteDatabase,
    SQLDatabaseDeps,
    SQLITE_SYSTEM_PROMPT,
    create_database_toolset,
)

async def main():
    async with SQLiteDatabase("chroma_db\chroma.sqlite3") as db:
        deps = SQLDatabaseDeps(database=db, read_only=True)
        toolset = create_database_toolset()

        agent = Agent(
            "groq:openai/gpt-oss-120b",
            deps_type=SQLDatabaseDeps,
            toolsets=[toolset],
            system_prompt=SQLITE_SYSTEM_PROMPT,
        )

        result = await agent.run(
            "Calculate Average Selling Price",
            deps=deps,
        )
        print(result.output)

    await main()