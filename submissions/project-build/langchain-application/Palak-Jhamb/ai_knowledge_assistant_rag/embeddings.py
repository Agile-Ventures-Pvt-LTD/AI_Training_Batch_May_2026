
from config import EMBEDDING_MODEL

from langchain_community.embeddings import SentenceTransformerEmbeddings


def get_embedding_model():
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings