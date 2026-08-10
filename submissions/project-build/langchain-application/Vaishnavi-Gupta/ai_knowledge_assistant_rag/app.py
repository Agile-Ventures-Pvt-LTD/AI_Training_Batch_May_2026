from loader import load_documents
from chunking import chunk_documents

from embeddings import get_embeddings

from vector_store import (
    create_vector_store,
    load_vector_store
)

from retriever import (
    get_retriever,
    retrieve_docs
)

from chains import (
    classify_query,
    generate_answer
)

from logger import log_query

from config import DATA_PATH


def build_index():

    docs = load_documents(DATA_PATH)
    chunks = chunk_documents(docs)

    embeddings = get_embeddings()

    vectordb = create_vector_store(
        chunks,
        embeddings
    )

    print(
        f"Indexed {len(chunks)} chunks"
    )

    return vectordb


def main():

    embeddings = get_embeddings()

    try:
        vectordb = load_vector_store(
            embeddings
        )

    except:
        vectordb = build_index()

    retriever = get_retriever(
        vectordb
    )

    while True:

        question = input(
            "\nAsk Question: "
        )

        if question.lower() == "exit":
            break

        classification = classify_query(
            question
        )

        docs = retrieve_docs(
            retriever,
            question
        )

        answer = generate_answer(
            question,
            docs
        )

        sources = []

        for d in docs:

            sources.append(
                {
                    "source_file":
                    d.metadata.get(
                        "source_file"
                    ),

                    "page_number":
                    d.metadata.get(
                        "page_number"
                    ),

                    "chunk_id":
                    d.metadata.get(
                        "chunk_id"
                    ),

                    "snippet":
                    d.page_content[:200]
                }
            )

        result = {
            "question": question,
            "query_type":
            classification.get(
                "query_type"
            ),
            "answer": answer,
            "sources": sources
        }

        print("\nANSWER\n")
        print(answer)

        print("\nSOURCES\n")
        for s in sources:
            print(s)

        print("\nDEBUG RETRIEVAL\n")
        for d in docs:

            print(
                d.metadata.get(
                    "chunk_id"
                )
            )

        log_query(result)


if __name__ == "__main__":
    main()