from langchain_chroma import Chroma

from config import VECTOR_STORE_DIR

def build_vector_store(chunks,embedding_model):
    vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=VECTOR_STORE_DIR
)

    return vectordb

def load_vector_store(embedding_model):
    return Chroma(
    persist_directory=VECTOR_STORE_DIR,
    embedding_function=embedding_model
)
