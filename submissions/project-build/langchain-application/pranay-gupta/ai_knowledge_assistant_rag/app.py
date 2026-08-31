import json
import os

from loaders import (load_pdf_documents)

from chunking import (chunk_documents,save_chunks)

from vector_store import (build_vector_store,load_vector_store)

from retriever import (get_retriever,retrieve_documents,build_context,extract_sources)

from chains import (classify_query,generate_answer)

from logger import (log_query)

from config import (RAW_DATA_PATH,VECTOR_DB_PATH)



def initialize_vector_db():

    print("Building vector store...")

    docs = load_pdf_documents(
        RAW_DATA_PATH
    )

    print("Documents Loaded:", len(docs))

    chunks = chunk_documents(docs)

    print("Chunks Created:", len(chunks))

    save_chunks(chunks)

    return build_vector_store(chunks)

def display_sources(sources):

    print("\n========================")

    print("SOURCES")

    print("========================")

    for source in sources:

        print(f"\nFile : {source['source_file']}")

        print(f"Page : {source['page_number']}")

        print(f"Chunk: {source['chunk_id']}")

        print(f"Snippet:\n{source['snippet']}")


def display_debug_view(docs):

    print("\n========================")

    print("RETRIEVAL DEBUG")

    print("========================")

    for idx, doc in enumerate(docs,start=1):

        print(f"\nChunk {idx}")

        print(f"Source : "f"{doc.metadata.get('source_file')}")

        print(
            f"Page : "
            f"{doc.metadata.get('page_number')}"
        )

        print(doc.page_content[:300])


def main():

    print("\nAI KNOWLEDGE ASSISTANT")

    vector_store = (initialize_vector_db())

    retriever = (get_retriever(vector_store))

    while True:

        question = input(
            "\nAsk Question "
            "(type exit to quit): "
        )

        if question.lower() == "exit":
            break

        try:

            classification = (
                classify_query(question)
            )

            query_type = (
                classification.get("query_type","OTHER")
            )

            retrieved_docs = (
                retrieve_documents(question,retriever)
            )

            if not retrieved_docs:

                print(
                    "\nI could not find "
                    "this information "
                    "in the provided documents."
                )

                continue

            context = (build_context(retrieved_docs))

            answer_data = (generate_answer(question,context))

            sources = (extract_sources(retrieved_docs))

            print("\n========================")

            print("ANSWER")

            print("========================")

            print(answer_data.get(
                    "answer",
                    "No answer generated."
                )
            )

            print("\nConfidence:",
                answer_data.get(
                    "confidence",
                    "LOW"
                )
            )

            print("\nAnswerability:",
                answer_data.get(
                    "answerability",
                    "NOT_FOUND"
                )
            )

            display_sources(sources)

            display_debug_view(retrieved_docs)

            log_query(
                question=question,
                query_type=query_type,
                retrieved_sources=sources,
                answer=answer_data.get(
                    "answer",
                    ""
                ),
                confidence=answer_data.get(
                    "confidence",
                    "LOW"
                ),
                answerability=answer_data.get(
                    "answerability",
                    "NOT_FOUND"
                )
            )

        except Exception as e:

            print(f"\nError: {str(e)}")



if __name__ == "__main__":
    main()