from langchain_huggingface import HuggingFaceEmbeddings

from config import settings


def get_embedding_model():

    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )