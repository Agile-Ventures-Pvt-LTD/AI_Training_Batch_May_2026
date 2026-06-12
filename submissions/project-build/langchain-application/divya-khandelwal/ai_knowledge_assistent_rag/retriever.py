from embedding import embedding
from langchain_chroma import Chroma


def retriver():

    # create embedding model
    embeddings = embedding()

    vector_db = Chroma(
        persist_directory="amazon_db",
        embedding_function=embeddings,
        collection_name="amazon-10k-2025"
    )

    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 5
        }
    )

    return retriever


if __name__ == "__main__":
    retriever = retriver()
    print("retriever done")