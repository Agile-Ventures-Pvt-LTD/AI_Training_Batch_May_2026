import pymupdf
from pathlib import Path

root_path = Path(__file__).parent.parent
pdf_path = root_path.joinpath("data/seller_guide.pdf")

doc = pymupdf.open("data/seller_guide.pdf")

# print(len(doc))

for page in doc:
    complete_txt = page.get_text()
#     # print(page.get_text())
#     print(complete_txt)
# print("\n=======================================\n")


from pydantic_ai import Embedder
embedder = Embedder('sentence-transformers:lightonai/DenseOn')
persist_directory = "./chroma_db"
chunk_collection_name = "seller_guide_collection"
import chromadb
chroma_client = chromadb.PersistentClient(
    path="./chroma_db",  # Local database
)
collection = chroma_client.get_or_create_collection(
        name=chunk_collection_name,
        metadata={"source": "seller_guide.pdf"}
    )
from typing import List

def chunk_document(document: str, chunk_size: int = 500) -> List[str]:
    """Split document into chunks"""
    words = document.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

async def add_documents(documents: List[str], metadatas: List[dict] = None):
    """Securely add documents to the system"""
    if not metadatas:
        metadatas = [{"source": f"doc_{i}"} for i in range(len(documents))]
    
    # Split documents into chunks
    chunks = []
    chunk_metadatas = []
    chunk_ids = []
    
    for i, (complete_txt, metadata) in enumerate(zip(documents, metadatas)):
        # Simple chunking (can be more sophisticated in real applications)
        doc_chunks = chunk_document(complete_txt, chunk_size=500)
        
        for j, chunk in enumerate(doc_chunks):
            chunks.append(chunk)
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "chunk_index": j,
                "total_chunks": len(doc_chunks)
            })
            chunk_metadatas.append(chunk_metadata)
            chunk_ids.append(f"doc_{i}_chunk_{j}")
    
    # Create embeddings locally
    embeddings = await embedder.embed_documents(chunks)
    
    
    # Add to Chroma (data remains local)
    collection.add(
        documents=chunks,
        metadatas=chunk_metadatas,
        ids=chunk_ids,
        # embeddings=embeddings
    )
    
    print(f"{len(chunks)} document chunks added securely")
    
await add_documents(complete_txt)


