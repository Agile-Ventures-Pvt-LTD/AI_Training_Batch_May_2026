import chromadb
from pypdf import PdfReader
from schema import DocsChunk
from langchain_chroma import Chroma

def pdf_chunks(pdf_location: str = "./data/seller_guide.pdf"):
    reader = PdfReader(pdf_location)
    no_of_pages = len(reader.pages)

    chunks = []

    for chunks_id in range(0, no_of_pages):
        chunks.append(DocsChunk(id=str(chunks_id), text=reader.pages[chunks_id].extract_text()))

    return chunks


try:
    chromadb_client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    vectorstore_persisted = Chroma(
        collection_name="seller_guide",
        collection_metadata={"hnsw:space": "cosine"},
        embedding_function=pdf_chunks,
        client=chromadb_client,
        persist_directory="./chroma_db"
    )

except Exception as e:
    print(e)