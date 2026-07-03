import os
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from config import MODEL_NAME

class KnowledgeBase:
    def __init__(self, pdf_path="data/Advanced_Business_Seller_Guide_May09.pdf", db_directoru="chroma_db"):
        self.pdf_path = pdf_path
        self.db_dir = db_directoru
        self.collection_name = "seller_guide_collection"
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=MODEL_NAME
        )
        self.chroma_client = chromadb.PersistentClient(path=self.db_dir)

    def chunking(self, text, chunk_size=800, chunk_overlap=150):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += (chunk_size - chunk_overlap)
        return chunks

    def vector_store(self):
        reader = PdfReader(self.pdf_path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        text_chunks = self._chunk_text(full_text)
        
        collection = self.chroma_client.create_collection(name=self.collection_name, embedding_function=self.embedding_fn)
        ids = [id for i in range(len(text_chunks))]
        collection.add(documents=text_chunks, ids=ids)
        return collection

    def user_query(self, user_query: str, result: int = 3) -> list:
        try:
            collection = self.chroma_client.get_collection(name=self.collection_name, embedding_function=self.embedding_fn)
        except Exception:
            collection = self.initialize_vector_store()

        results = collection.query(query_texts=[user_query], result=result)
        return results["documents"] if results["documents"] else []
