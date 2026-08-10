import os
import re
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.config import Config
import sys

def load_pdf_documents():
    """
    Loads PDF documents from the directory specified in Config.
    """
    print(f"Attempting to load documents from: {Config.DATA_DIR}")
    
    loader = DirectoryLoader(
        str(Config.DATA_DIR),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    
    docs = loader.load()


    for doc in docs:
        source_path = doc.metadata.get("source", "")
        file_name = os.path.basename(source_path)
        
        year_match = re.search(r'\b(20|19)\d{2}\b', file_name)
        
        doc.metadata["source_file"] = file_name
        doc.metadata["page_number"] = doc.metadata.get("page", 0) + 1
        doc.metadata["document_type"] = "PDF"
        doc.metadata["year"] = year_match.group(0) if year_match else "Unknown"

    return docs



def get_text_chunks(documents):
    """
    Splits a list of documents into smaller chunks based on Config settings.
    Adds metadata about the start index for better traceability.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
    )
    
    chunks = text_splitter.split_documents(documents)

    # Assign unique chunk_ids using the enriched metadata
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source_file", "doc")
        page = chunk.metadata.get("page_number", 0)
        content = chunk.page_content
        # Extracting the first line of the chunk as a heuristic for section_title
        first_line = content.partition('\n')[0].strip()

        chunk.metadata["chunk_id"] = f"{source}_p{page}_c{i}"
        chunk.metadata["section_title"] = first_line[:100] if first_line else "Unknown Section"
        chunk.metadata["text"] = content

    print(f"Created {len(chunks)} chunks from {len(documents)} document pages.")
    return chunks


def get_embedding_model():
    """
    Initializes and returns the HuggingFace embedding model.
    """
    return HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL_NAME
    )

def create_vector_store(chunks):
    """
    Creates a Chroma vector store from document chunks and persists it to disk.
    """
    embeddings = get_embedding_model()
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(Config.VECTOR_STORE_DIR)
    )
    
    print(f"Vector store successfully created at: {Config.VECTOR_STORE_DIR}")
    return vector_store


def run_ingestion():
    """Runs the ingestion pipeline to build the vector store."""
    print("Step 1: Loading PDF documents...")
    docs = load_pdf_documents()
    if not docs:
        print("Error: No PDF documents found in data/raw/.")
        sys.exit(1)

    print(f"Step 2: Splitting {len(docs)} pages into chunks...")
    chunks = get_text_chunks(docs)
    
    print("Step 3: Generating embeddings and updating Vector Store...")
    create_vector_store(chunks)
    print("--- Ingestion Complete ---\n")



def main():
    print("--- AI Knowledge Assistant (CLI) ---")

    # Check if vector store exists, if not, ingest
    if not Config.VECTOR_STORE_DIR.exists() or not any(Config.VECTOR_STORE_DIR.iterdir()):
        print("Vector store not found. Starting initial ingestion...")
        run_ingestion()
    else:
        print(f"Existing Vector Store found at {Config.VECTOR_STORE_DIR}. Skipping ingestion.")


if __name__ == "__main__":
    main()