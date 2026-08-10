from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL
def get_embedding_model():

    embedding_model = embedding_model=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    return embedding_model