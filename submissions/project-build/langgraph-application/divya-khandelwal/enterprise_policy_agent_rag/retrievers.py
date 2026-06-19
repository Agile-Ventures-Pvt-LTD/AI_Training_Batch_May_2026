from chunking import embedding
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv
load_dotenv()

def retriver():

    # create embedding model
    embeddings = embedding()

    vector_db = Chroma(
        persist_directory="vector_store",
        embedding_function=embeddings,
        collection_name="enterprise-policy-data"
    )

    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": int(os.getenv("TOP_K"))
        }
    )

    return retriever


if __name__ == "__main__":
    retriever = retriver()
    print("retriever done")