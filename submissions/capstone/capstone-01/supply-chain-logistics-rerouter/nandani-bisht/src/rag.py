import os
from typing import List
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings, embeddings
from langchain_community.vectorstores import FAISS

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

KNOWLEDGE_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "logistics_knowledge_base.txt"
)


_vectorstore = None
_retriever = None

def initialize_rag() -> None:
    """Initialize the FAISS vector database from the logistics knowledge base file."""
    global _vectorstore, _retriever
    
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        raise FileNotFoundError(f"Knowledge base file not found at: {KNOWLEDGE_BASE_PATH}")
        
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    _vectorstore = FAISS.from_documents(documents, embedding_model)
    
    _retriever = _vectorstore.as_retriever(search_kwargs={"k": 2})

def retrieve_relevant_rules(query: str) -> List[str]:
    """
    Retrieve relevant logistics rules matching the query.
    
    Args:
        query: The query string (e.g. incident manifest text).
        
    Returns:
        A list of matching rule strings.
    """
    global _retriever
    if _retriever is None:
        initialize_rag()
        
    docs = _retriever.invoke(query)
    return [doc.page_content for doc in docs]