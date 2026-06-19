from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def process_and_chunk_documents(raw_documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )

    all_final_chunks = []

    for doc in raw_documents:
        heading_splits = markdown_splitter.split_text(doc.page_content)
        
        final_splits = text_splitter.split_documents(heading_splits)
        
        for split in final_splits:
            split.metadata["source"] = doc.metadata.get("source")
            all_final_chunks.append(split)

    return all_final_chunks
