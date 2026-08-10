from langchain_huggingface import HuggingFaceEmbeddings
from config import Config

def embedder():
    """converting the chunks into numerical value for storage"""
    embedding = HuggingFaceEmbeddings(
        model_name = Config.EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    return embedding