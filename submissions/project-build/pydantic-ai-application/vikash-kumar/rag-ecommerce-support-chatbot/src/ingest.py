import os
import uuid
import chromadb
from chromadb.utils import embedding_functions
from PyPDF2 import PdfReader

def sliding_window_chunk(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list:
    """Splits raw text strings into overlapping structural blocks."""
    chunks = []
    start = 0
    if not text:
        return chunks
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def build_persistent_vector_db(pdf_path: str, db_dir: str = "./ecommerce_bot_db"):
    """Extracts text from PDF, processes chunks, and writes them to local disk."""
    print(f"Reading documentation from: {pdf_path}")
    reader = PdfReader(pdf_path)
    
    all_chunks = []
    all_metadata = []
    
    # Process page by page to capture correct source metadata
    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text()
        page_num = page_idx + 1
        
        # Segment the specific page content
        page_chunks = sliding_window_chunk(page_text, chunk_size=600, chunk_overlap=120)
        
        for chunk_idx, chunk_string in enumerate(page_chunks):
            all_chunks.append(chunk_string)
            all_metadata.append({
                "source_file": os.path.basename(pdf_path),
                "page_number": page_num,
                "chunk_index": chunk_idx
            })

    if not all_chunks:
        print("Error: No text extracted from the document.")
        return

    print(f"Generated {len(all_chunks)} text segments. Initializing database storage...")

    # Initialize persistent storage path
    client = chromadb.PersistentClient(path=db_dir)
    
    # Force localized embedding generation to prevent WinError connection refusals
    local_embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Establish collection bindings
    collection = client.get_or_create_collection(
        name="ebay_seller_policies",
        embedding_function=local_embedder
    )
    
    # Formulate deterministic primary keys
    unique_ids = [str(uuid.uuid4()) for _ in all_chunks]
    
    # Save elements downstream to database files
    collection.add(
        documents=all_chunks,
        metadatas=all_metadata,
        ids=unique_ids
    )
    
    print(f"Success! Data securely written locally to directory: '{db_dir}'")

if __name__ == "__main__":
    # Ensure dependencies are available: pip install chromadb sentence-transformers pypdf2
    pdf_filename = "Advanced_Business_Seller_Guide.pdf"
    
    if os.path.exists(pdf_filename):
        build_persistent_vector_db(pdf_path=pdf_filename)
    else:
        print(f"Please place your '{pdf_filename}' file inside this exact folder directory to execute.")
