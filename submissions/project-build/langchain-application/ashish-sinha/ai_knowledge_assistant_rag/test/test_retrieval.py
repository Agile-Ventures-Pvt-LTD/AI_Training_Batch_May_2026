
from vector_store import load_vector_store
from retriever import Retriever

def test_retrieval():

    vector_store = load_vector_store()

    retriever = Retriever(
        vector_store
    )

    query = (
        "What are the main business segments?"
    )

    docs = retriever.retrieve(
        query
    )

    print(f"\nRetrieved {len(docs)} documents")

    print("\nQUERY:")
    print(query)

    print("\nRETRIEVED CHUNKS:")

    for idx, doc in enumerate(
        docs,
        start=1
    ):

        print(
            f"\nRank: {idx}"
        )

        print(
            "Source:",
            doc.metadata.get(
                "source_file"
            )
        )

        print(
            "Page:",
            doc.metadata.get(
                "page_number"
            )
        )

        print(
            "Chunk:",
            doc.metadata.get(
                "chunk_id"
            )
        )

        print(
            "Similarity:",
            doc.metadata.get(
                "similarity_score"
            )
        )

        print(
            "\nPreview:"
        )

        print(
            doc.page_content[:500]
        )


if __name__ == "__main__":

    test_retrieval()