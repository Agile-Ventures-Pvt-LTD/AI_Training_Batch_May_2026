import os

from loaders import load_documents
from chunking import create_chunks
from embeddings import get_embedding_model

from vector_store import (
    build_vector_store,
    load_vector_store
)

from retriever import (
    get_retriever,
    retrieve_context
)

from chains import (
    classify_query,
    generate_answer
)

from output_parser import build_sources

from logger import log_query

from config import RAW_DATA


def build_index():

    print("Loading the documents from pdf")

    docs = load_documents(
        RAW_DATA
    )

    if not docs:
        raise ValueError(
            "No documents found in data/raw/"
        )

    chunks = create_chunks(docs)

    print(
        f"Created {len(chunks)} chunks"
    )

    embedding_model = (
        get_embedding_model()
    )

    build_vector_store(
        chunks,
        embedding_model
    )

    print(
        f"Vector store created with {len(chunks)} chunks"
    )


def ask_question(question):
    embedding_model = (
        get_embedding_model()
    )

    vector_db = load_vector_store(
        embedding_model
    )

    retriever = get_retriever(
        vector_db
    )

    query_type = classify_query(
        question
    )

    print("QUERY TYPE")
    print(query_type.content)

    docs = retrieve_context(
        retriever,
        question
    )

    if not docs:
        print(
            "No relevant chunks found as per the user query."
        )
        return

    answer = generate_answer(
        question,
        docs
    )

    sources = build_sources(
        docs
    )

    print("ANSWER")
    print(answer.content)
    print("SOURCES")

    for source in sources:
        print(
            f"File: {source['source_file']}"
        )

        print(
            f"Page: {source['page_number']}"
        )

        print(
            f"Chunk: {source['chunk_id']}"
        )

        print(
            f"Snippet: {source['snippet']}"
        )

    log_query(
        {
            "question": question,
            "query_type": query_type.content,
            "answer": answer.content,
            "sources": sources
        }
    )


if __name__ == "__main__":

    if not os.path.exists(
        "data/vector_store/chroma.sqlite3"):
        print("Creating vector store")
        build_index()

    else:
        print("Using existing vector store")

    while True:

        question = input(
            "Ask Question (type exit to quit): "
        )

        if question.lower() == "exit":
            break

        ask_question(question)