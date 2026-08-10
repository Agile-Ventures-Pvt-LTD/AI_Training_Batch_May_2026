from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Config

def txt_splitting_to_chunks(document):
    """splitting documents into smaller chunks for better accuracy and overlapping for good retrivel"""
    if not document:
        return []
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = Config.CHUNK_SIZE,
        chunk_overlap = Config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = splitter.split_documents(document)
    
    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk_{idx:05d}"
        
    return chunks