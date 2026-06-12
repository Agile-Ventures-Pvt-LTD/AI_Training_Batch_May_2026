from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Config

def get_text_chunks(documents):
    """
    Splits a list of documents into smaller chunks based on Config settings.
    Adds metadata about the start index for better traceability.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=Config.CHUNK_SIZE,chunk_overlap=Config.CHUNK_OVERLAP,length_function=len,add_start_index=True,)
    
    chunks = text_splitter.split_documents(documents)
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source_file", "doc")
        page = chunk.metadata.get("page_number", 0)
        content = chunk.page_content
        first_line = content.partition('\n')[0].strip()
        chunk.metadata["chunk_id"] = f"{source}_p{page}_c{i}"
        chunk.metadata["section_title"] = first_line[:100] if first_line else "Unknown Section"
        chunk.metadata["text"] = content

    print(f"Created {len(chunks)} chunks from {len(documents)} document pages.")
    return chunks