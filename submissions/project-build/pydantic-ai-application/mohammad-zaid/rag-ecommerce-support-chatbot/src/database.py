import os
from pathlib import Path
from typing import List
import pymupdf
import chromadb
from pydantic_ai import Embedder

# Initialize paths
ROOT_PATH = Path(__file__).parent.parent
DATA_PATH = ROOT_PATH.joinpath("data/seller_guide.pdf")
PERSIST_DIRECTORY = ROOT_PATH.joinpath("chroma_db")
CHUNK_COLLECTION_NAME = "seller_guide_collection"

# Initialize embedder
embedder = Embedder('sentence-transformers:lightonai/DenseOn')

# Initialize Chroma client with persistent storage
chroma_client = chromadb.PersistentClient(
    path=str(PERSIST_DIRECTORY),
)

def get_or_create_collection():
    """Get or create the collection for document chunks"""
    collection = chroma_client.get_or_create_collection(
        name=CHUNK_COLLECTION_NAME,
        metadata={"source": "seller_guide.pdf"}
    )
    return collection

def chunk_document(document: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split document into chunks with overlap to maintain context
    """
    words = document.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        # Break if we've reached the end
        if i + chunk_size >= len(words):
            break
            
    return chunks

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF using PyMuPDF"""
    doc = pymupdf.open(pdf_path)
    complete_text = ""
    
    for page in doc:
        complete_text += page.get_text() + "\n"
        
    return complete_text

async def initialize_database(force_reset=False):
    """
    Initialize the database with document chunks.
    Only creates embeddings if the database doesn't exist or force_reset is True.
    """
    # Check if database already exists
    if os.path.exists(PERSIST_DIRECTORY) and not force_reset:
        print("Database already exists. Skipping initialization.")
        return get_or_create_collection()
    
    # Create fresh database if needed
    if force_reset and os.path.exists(PERSIST_DIRECTORY):
        import shutil
        shutil.rmtree(PERSIST_DIRECTORY)
    
    # Extract text from PDF
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"PDF file not found at {DATA_PATH}. Please download it first.")
    
    print("Extracting text from PDF...")
    document_text = extract_text_from_pdf(DATA_PATH)
    
    # Chunk the document
    print("Chunking document...")
    chunks = chunk_document(document_text)
    print(f"Created {len(chunks)} chunks")
    
    # Create embeddings
    print("Creating embeddings...")
    embeddings = await embedder.embed_documents(chunks)
    
    # Get or create collection
    collection = get_or_create_collection()
    
    # Prepare metadata and IDs
    metadatas = [{"chunk_index": i, "total_chunks": len(chunks), "source": "seller_guide.pdf"} 
                 for i in range(len(chunks))]
    ids = [f"doc_chunk_{i}" for i in range(len(chunks))]
    
    # Add to collection
    print("Adding to Chroma DB...")
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Successfully added {len(chunks)} chunks to the database")
    return collection

def retrieve_documents(query: str, n_results: int = 5) -> List[str]:
    """
    Retrieve relevant documents for a query from Chroma DB
    """
    collection = get_or_create_collection()
    
    results = collection.query(
        query_texts=query,
        n_results=n_results,
    )
    
    # Extract just the document texts
    documents = results['documents'][0] if results['documents'] else []
    return documents