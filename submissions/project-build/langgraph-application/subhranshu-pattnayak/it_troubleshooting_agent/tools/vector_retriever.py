from langchain.tools.retriever import create_retriever_tool
from utils.paths import vector_path, collection_name
from rag_core.embedding import init_embedding
from langchain_groq import Chroma

embedding_model = init_embedding()

def retriever():
    vectorstore_persisted = Chroma(
        collection_name=collection_name,
        collection_metadata={"hnsw:space": "cosine"},
        persist_directory=vector_path,
        embedding_function=embedding_model
    )
    
    retriever = vectorstore_persisted.as_retriever(search_kwargs={'k': 5})
    
    return create_retriever_tool(
        retriever,
        "retrieve_",
        "Search and return information about the given issue."
    )

retrieve_tool = retriever()