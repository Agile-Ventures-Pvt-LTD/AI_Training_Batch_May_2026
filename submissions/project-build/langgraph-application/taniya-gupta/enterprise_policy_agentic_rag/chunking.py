from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import config

class Chunker:
    def __init__(self, chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP):
        self.splitter=RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    def split_documents(self,documents):
        chunks=self.splitter.split_documents(documents)
        for i, chunk in enumerate(chunks):
            source=chunk.metadata.get("source_file", "could not get source")
            chunk.metadata["chunk_id"]=f"{source}_chunk_{i:03d}"
        return chunks