from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)
    chunks = text_splitter.split_documents(documents)

    return chunks

# from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
# from config import CHUNK_SIZE, CHUNK_OVERLAP

# def create_chunks(documents):
#     headers_to_split_on = [
#         ("#", "Header_1"),
#         ("##", "Header_2"),
#         ("###", "Header_3"),
#     ]
#     markdown_splitter = MarkdownHeaderTextSplitter(
#         headers_to_split_on=headers_to_split_on,
#         strip_headers=False
#     )
#     recursive_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         encoding_name='cl100k_base',
#         chunk_size=CHUNK_SIZE,
#         chunk_overlap=CHUNK_OVERLAP
#     )
    
#     final_chunks = []
    
#     for doc in documents:
#         header_splits = markdown_splitter.split_text(doc.page_content)

#         for split in header_splits:
#             split.metadata.update(doc.metadata)
            
#         sub_splits = recursive_splitter.split_documents(header_splits)
#         final_chunks.extend(sub_splits)

#     return final_chunks
