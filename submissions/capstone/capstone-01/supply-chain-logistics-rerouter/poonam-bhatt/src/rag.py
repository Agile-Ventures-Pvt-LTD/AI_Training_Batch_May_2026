import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

_retriever = None

def get_retriever():
    """Initializes and returns the RAG retriever using local FAISS and HuggingFace embeddings."""
    global _retriever
    if _retriever is not None:
        return _retriever

    kb_path = "data/logistics_knowledge_base.txt"         # txt_path
    if not os.path.exists(kb_path):
        raise FileNotFoundError(f"Knowledge base file not found at: {kb_path}")

    #-------------------------------
    # Load and split
    #-------------------------------

    loader = TextLoader(kb_path, encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,                                                  # since data is too small
        chunk_overlap=30
    )
    chunks = splitter.split_documents(documents)


    #--------------------------------------------------
    # Embeddings (local sentence-transformers model)
    #--------------------------------------------------
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    #----------------------------------------------------------
    # In-memory FAISS database (Mentioned in PRD to use FAISS)
    #----------------------------------------------------------
    
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
        
    )
    

    _retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return _retriever

def retrieve_logistics_rules(query: str) -> str:
    """Retrieves logistics rules from the knowledge base relevant to the query."""
    try:
        retriever = get_retriever()
        docs = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error retrieving rules: {str(e)}"





### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026