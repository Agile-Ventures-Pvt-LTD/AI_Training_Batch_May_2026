from langchain_chroma import Chroma

from embeddings import get_embedding_model
from config import settings


COLLECTION_NAME = "enterprise_docs"


def build_vector_store(chunks):

    embeddings = get_embedding_model()

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(
            settings.VECTOR_DB_DIR
        ),
        collection_name=COLLECTION_NAME
    )

    return db


def load_vector_store():

    db = Chroma(
        persist_directory=str(
            settings.VECTOR_DB_DIR
        ),
        embedding_function=(
            get_embedding_model()
        ),
        collection_name=COLLECTION_NAME
    )

    return db