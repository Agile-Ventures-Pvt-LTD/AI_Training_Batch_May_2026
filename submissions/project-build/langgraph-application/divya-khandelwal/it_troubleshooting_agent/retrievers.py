import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from loaders import embedding

load_dotenv()


def create_retriever():
    embeddings = embedding()

    vector_db = Chroma(
        persist_directory=os.getenv("VECTOR_STORE_PATH", "vector_store"),
        embedding_function=embeddings,
        collection_name="enterprise-policy-data",
    )

    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": int(os.getenv("TOP_K", "4"))
        },
    )
    return retriever


retriever = create_retriever()


if __name__ == "__main__":
    print("retriever initialized")