import os
import chromadb
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

class LogisticsRAGPipeline:
    def __init__(self):
        data_path = os.path.join(DATA_DIR, "logistics_knowledge_base.txt")
        if not os.path.exists(data_path):
            raise FileNotFoundError("File is missing")
            
        loader = TextLoader(data_path, encoding="utf-8")
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=40)
        chunks = text_splitter.split_documents(documents)
        
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        database_path="chroma.db"
        client = chromadb.PersistentClient(path=database_path)
        
        self.vector_store = Chroma.from_documents(documents=chunks,embedding=self.embeddings,client=client)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 2})

    def retrieve_rules(self, query: str) -> str:
        try:
            docs = self.retriever.invoke(query)
            return "\n---\n".join([doc.page_content for doc in docs])
        except Exception as e:
            return f"Error occured: {str(e)}"
