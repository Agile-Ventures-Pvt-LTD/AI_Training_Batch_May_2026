import time
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def initialize():
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    pdf_folder_location = "data/Advanced_Business_Seller_Guide_May09.pdf"
    pdf_loader = PyPDFLoader(pdf_folder_location)
    documents=pdf_loader.load()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size=510,
    chunk_overlap=16
)
    ebay_chunks = text_splitter.split_documents(documents)
    ebay_collection = 'ebay_collection'
    chromadb_client = chromadb.PersistentClient(
    path="./chroma_db"
)
    vectorstore = Chroma(
    collection_name=ebay_collection,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding,
    client=chromadb_client,
    persist_directory="./chroma_db"
)
    i = 0 
    while i < len(ebay_chunks): 
        vectorstore.add_documents( 
        documents=ebay_chunks[i:i+500], 
        ids=["text_" + str(i) for i in range(i, i+500)] 
        )
        i += 500 
        time.sleep(5) 

    return vectorstore

class ChromaEmbeddingWrapper(chromadb.EmbeddingFunction):
    def __init__(self, langchain_embeddings):
        self.langchain_embeddings = langchain_embeddings

    def __call__(self, input):
        return self.langchain_embeddings.embed_documents(input)

def get_collection():
    client=chromadb.PersistentClient("chroma_db")
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return client.get_collection(
        name="ebay_collection",
        embedding_function=ChromaEmbeddingWrapper(embedding)
    )

def retriever(query,n=5): 
    collection = get_collection()
    results=collection.query(
        query_texts=query,
        n_results=n
    )
    documents = results.get("documents")[0]
    metadatas = results.get("metadatas")[0]
    
    context_parts = []
    for doc, meta in zip(documents, metadatas):
        context_parts.append(f"[Page {meta['page']}]: {doc}")
        
    return "\n\n".join(context_parts)