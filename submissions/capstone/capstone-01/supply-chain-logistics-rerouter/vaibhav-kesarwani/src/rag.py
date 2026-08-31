import os 
import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

LOGISTIC_PATH = "./data/logistics_knowledge_base.txt"

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

try:
    with open(LOGISTIC_PATH, "r") as f:
        data = f.read()
    
except Exception as e:
    print(f"Error Loading the Logistics File : {e}")


text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=16)
texts = text_splitter.split_text(data)

chromadb_client = chromadb.PersistentClient(
    path="./logistic_incident"
)

vectorstore = Chroma(
    collection_name="logistic_incident",
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding,
    client=chromadb_client,
    persist_directory="./logistic_incident"
)

vectorstore.add_texts(texts=texts)


retriever = vectorstore.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 4}
)