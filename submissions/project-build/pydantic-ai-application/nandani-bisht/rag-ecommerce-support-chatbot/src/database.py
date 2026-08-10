import os
import shutil
import pypdf
import chromadb
from chromadb.utils import embedding_functions

DB_DIR = "./chroma_db"
RAW_PDF_PATH = "./data/Advanced_Business_Seller_Guide_May09.pdf"
PDF_PATH = "./data/seller_guide.pdf"
COLLECTION_NAME = "seller_guide"

def get_chroma_client():
    """Initializes and returns the persistent Chroma DB client."""
    return chromadb.PersistentClient(path=DB_DIR)

def get_embedding_function():
    """Returns the local SentenceTransformer embedding function."""
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

def copy_pdf_if_needed():
    """Ensures raw PDF is copied/renamed exactly as seller_guide.pdf in data/."""
    os.makedirs("./data", exist_ok=True)
    if os.path.exists(RAW_PDF_PATH) and not os.path.exists(PDF_PATH):
        print(f"Copying {RAW_PDF_PATH} to {PDF_PATH}...")
        shutil.copy(RAW_PDF_PATH, PDF_PATH)
    elif not os.path.exists(PDF_PATH):
        print(f"Warning: {RAW_PDF_PATH} not found. Please ensure PDF is placed in data/.")

def chunk_text(text: str, page_num: int, chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    """
    Splits text into chunks of specified size and overlap recursively.
    Returns a list of dictionaries with 'text' and 'metadata'.
    """
    chunks = []
    if len(text) <= chunk_size:
        return [{"text": text, "metadata": {"page": page_num, "char_count": len(text)}}]

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append({
            "text": chunk,
            "metadata": {
                "page": page_num,
                "char_count": len(chunk)
            }
        })
        start += (chunk_size - overlap)
        
    return chunks

def load_and_chunk_pdf() -> list[dict]:
    """Loads PDF pages and generates chunked documents with page metadata."""
    copy_pdf_if_needed()
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF file not found at {PDF_PATH}")
        
    print(f"Reading PDF from {PDF_PATH}...")
    reader = pypdf.PdfReader(PDF_PATH)
    all_chunks = []
    
    for page_idx, page in enumerate(reader.pages):
        page_num = page_idx + 1
        text = page.extract_text() or ""
        text = text.strip()
        if not text:
            continue
            
        page_chunks = chunk_text(text, page_num)
        all_chunks.extend(page_chunks)
        
    print(f"Generated {len(all_chunks)} chunks from PDF.")
    return all_chunks

def initialize_database():
    """
    Initializes the persistent vector store.
    Only embeds and indexes if the collection is empty or does not exist.
    """
    client = get_chroma_client()
    emb_fn = get_embedding_function()
    

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )
    

    count = collection.count()
    if count > 0:
        print(f"Chroma DB collection '{COLLECTION_NAME}' already initialized with {count} documents.")
        return collection
        
    print("Initializing Chroma DB collection from scratch...")
    chunks = load_and_chunk_pdf()
    

    documents = []
    metadatas = []
    ids = []
    
    for idx, c in enumerate(chunks):
        documents.append(c["text"])
        metadatas.append(c["metadata"])
        ids.append(f"chunk_{idx:05d}")
        

    batch_size = 100
    for i in range(0, len(documents), batch_size):
        end_idx = i + batch_size
        collection.add(
            documents=documents[i:end_idx],
            metadatas=metadatas[i:end_idx],
            ids=ids[i:end_idx]
        )
        print(f"Inserted chunks {i} to {min(end_idx, len(documents))}")
        
    print(f"Successfully database initialization. Total indexed chunks: {collection.count()}")
    return collection

if __name__ == "__main__":
    initialize_database()
