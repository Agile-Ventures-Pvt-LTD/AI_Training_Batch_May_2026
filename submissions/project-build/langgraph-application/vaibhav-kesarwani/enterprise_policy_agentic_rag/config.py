import os
import chromadb
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")

try:
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    chromadb_client = chromadb.PersistentClient(
        path="./vector_store"
    )

    llm = ChatGroq(
        model=os.environ["GROQ_MODEL"], 
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0
    )
except Exception as e:
    print(e)