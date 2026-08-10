from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from langchain_chroma import chroma
import time

loader = PyPDFDirectoryLoader(
    "it_support",
    glob="*.pdf"
)

pdf_folder_location = "it_support"

pdf_loader = PyPDFDirectoryLoader(pdf_folder_location)

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size=900,
    chunk_overlap=120
)

it_support_chunks = pdf_loader.load_and_split(text_splitter)
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

chromadb_client = chromadb.PersistentClient(
    path="./it_support_db"
)

vectorstore = Chroma(
    collection_name=it_support_chunks,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding,
    client=chromadb_client,
    persist_directory="./it_support_db"
)

i = 0 

while i < len(it_support_chunks): 
    vectorstore.add_documents( 
        documents=it_support_chunks[i:i+500], 
        ids=["text_" + str(i) for i in range(i, i+500)]
    )

    i += 500 
    time.sleep(30) 