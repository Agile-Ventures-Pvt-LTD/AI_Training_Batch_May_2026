from vector_store import (load_vector_store)

from retriever import (get_retriever)


def test_retrieval():

    vectordb = (load_vector_store())

    retriever = (get_retriever(vectordb))

    docs = retriever.invoke("What are Amazon's business segments?")

    assert len(docs) > 0

    print("\nRetrieval test passed.")


if __name__ == "__main__":
    test_retrieval()