from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from chunking import chunks

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    collection_name="md_collection",
    embedding_function=embeddings,
    persist_directory="./vector_store" 
)

db.add_documents(chunks)
db.persist()

print("Stored in Chroma.")