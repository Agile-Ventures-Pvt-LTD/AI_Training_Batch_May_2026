from pathlib import Path
import json

from loaders import load_documents
from chunking import chunk_documents

from vector_store import build_vector_store
from retriever import retrieve_documents

from chains import build_chain
from output_parser import format_output

from logger import save_log


def index_documents():

    print("\nLoading documents...")

    docs = load_documents()

    print("\nChunking documents...")

    chunks = chunk_documents(docs)

    print("\nCreating vector store...")

    build_vector_store(chunks)

    print("\nIndex completed")


def save_benchmark(result):

    output_file = Path(
        "outputs/benchmark_results.json"
    )

    output_file.parent.mkdir(
        exist_ok=True
    )

    if output_file.exists():

        with open(
            output_file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(
                f
            )

    else:

        data = []

    data.append(
        result
    )

    with open(

        output_file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=2,

            ensure_ascii=False
        )


def ask_questions():

    chain = build_chain()

    while True:

        question = input(
            "\nAsk Question: "
        )

        if question.lower() == "exit":
            break

        if not question.strip():

            print(
                "\nEnter valid question"
            )

            continue

        docs = retrieve_documents(
            question
        )

        if len(docs) == 0:

            print(
                "\nNOT_FOUND"
            )

            continue

        context = "\n\n".join(

            doc.page_content

            for doc in docs
        )

        answer = chain.invoke(
            {
                "question":
                question,

                "context":
                context
            }
        )

        result = format_output(
            answer,
            docs
        )

        print("\nAnswer:\n")

        print(
            result["answer"]
        )

        print("\nSources:\n")

        for source in result[
            "sources"
        ]:

            print(
                f"Page {source['page']} | "
                f"{source['chunk']}"
            )

        save_log(
            result
        )

        save_benchmark(
            result
        )


if __name__ == "__main__":

    db_path = Path(
        "data/vector_store"
    )

    if not db_path.exists():

        index_documents()

    ask_questions()
