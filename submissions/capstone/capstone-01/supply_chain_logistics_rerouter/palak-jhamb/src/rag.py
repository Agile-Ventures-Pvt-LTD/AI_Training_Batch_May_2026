from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.document_loaders import TextLoader
import os 
from dotenv import load_dotenv
load_dotenv()
os.environ["CHUNK_SIZE"]=os.getenv("CHUNK_SIZE")
os.environ["CHUNK_OVERLAP"]=os.getenv("CHUNK_OVERLAP")
os.environ["file_path"]=os.getenv("file_path")
os.environ["EMBEDDING_MODEL"]=os.getenv("EMBEDDING_MODEL")
faiss_save_path=os.getenv("faiss_save_path")
from langchain_community.vectorstores import FAISS

#load pdf from path
def load_documents():
    file_path=os.environ["file_path"]
    loader = TextLoader(
            file_path=file_path,
            encoding="utf-8"
        )

    docs = loader.load() 
    return docs
    
# split data using recursive text splitter
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=int(os.environ["CHUNK_SIZE"]), chunk_overlap=int(os.environ["CHUNK_OVERLAP"]))
    texts = text_splitter.split_documents(documents)
    return texts

#get embedding model from hugging face
def get_embedding_model():
    embeddings = SentenceTransformerEmbeddings(model_name=os.environ["EMBEDDING_MODEL"])
    return embeddings

#this is a function used to create faiss vector db
def create_faiss_db():
    documents = load_documents()
    chunks= split_documents(documents)
    embedding_model = get_embedding_model()
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(faiss_save_path)
    print("vector store created ")




