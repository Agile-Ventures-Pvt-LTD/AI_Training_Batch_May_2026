import json

from loaders import load_documents
from chunking import chunk_documents
from vector_store import create_vector_store, load_vector_store
from chains import RAGChains
from output_parser import parse_output
from logger import log_query
from config import RAW_DATA_PATH


def build_index():

    print("\nLoading Documents...")

    docs = load_documents(RAW_DATA_PATH)

    if not docs:

        raise ValueError("No documents found.")

    print(f"Loaded {len(docs)} pages")

    print("\nChunking...")

    chunks = chunk_documents(docs)

    print(f"Created {len(chunks)} chunks")

    print("\nCreating Vector Store...")

    create_vector_store(chunks)

    print("Index Built Successfully.")


def run_chat():

    vector_store = (load_vector_store())

    rag = RAGChains(vector_store)

    while True:

        question = input("\nAsk Question (or 'exit'): ")

        if question.lower() == "exit":
            break

        query_info = (rag.classify_query(question))

        query_type = ( query_info.get("query_type","OTHER"))

        docs = rag.retriever.retrieve( question)

        response = (rag.generate_answer(question))

        parsed = parse_output(response)

        sources = ( rag.get_sources(docs))

        print("\nAnswer\n")

        print(parsed.get(  "answer",""))

        print("\nConfidence:",parsed.get("confidence","LOW"))

        print("\nAnswerability:",parsed.get("answerability","NOT_FOUND"))

        print("\nSources\n")

        for src in sources:

            print(json.dumps(  src,indent=2))

        log_query(
            question=question,
            query_type=query_type,
            retrieved_sources=sources,
            answer=parsed.get("answer",""),
            answerability=parsed.get("answerability", ""),
            confidence=parsed.get( "confidence","")
        )


if __name__ == "__main__":

    print("\nAI Knowledge Assistant")

    print("\n1. Build Index")

    print("2. Ask Questions")

    choice = input("\nEnter Choice: ")

    if choice == "1":

        build_index()

    elif choice == "2":

        run_chat()

    else:

        print("Invalid Choice")