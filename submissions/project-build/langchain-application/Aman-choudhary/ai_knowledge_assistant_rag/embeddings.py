from langchain_community.embeddings import HuggingFaceEmbeddings
from config import Config

def get_embedding_model():
    """
    Initializes and returns the HuggingFace embedding model.
    """
    return HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL_NAME
    )