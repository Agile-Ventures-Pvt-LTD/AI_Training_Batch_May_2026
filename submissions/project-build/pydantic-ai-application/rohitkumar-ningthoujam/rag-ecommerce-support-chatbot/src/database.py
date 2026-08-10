import time
import chromadb

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document

from langchain_core import chat_loaders
from langchain_community.embeddings import HuggingFaceEmbeddings

from pathlib import Path
pdf_folder_location= Path("data/Advanced_Business_Seller_Guide_May09.pdf").resolve()
print("Loading PDFs from:", pdf_folder_location)


pdf_loader = PyPDFDirectoryLoader(str(pdf_folder_location))

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size = 1000,
    chunk_overlap=100
)

advanced_B_chunk = pdf_loader.load_and_split(text_splitter)

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

chromadb_client = chromadb.PersistentClient(
    path="./advanced_Business_Seller_Guide_May09.pdf"
)

vectorstore = Chroma(
    collection_name = advanced_B_chunk ,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding,
    client=chromadb_client,
    persist_directory="./advanced_Business_Seller_Guide_May09.pdf"
)

i = 0 

while i < len(advanced_B_chunk):
    batch = advanced_B_chunk[i:i+500] 
    ids = ["text_" + str(j) for j in range(i, i + len(batch))] 
    vectorstore.add_documents( 
         documents=batch,
        ids=ids
    )

    i += len(batch) 
    time.sleep(0.5) 
 
retriever = vectorstore_persisted.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 5}
)
