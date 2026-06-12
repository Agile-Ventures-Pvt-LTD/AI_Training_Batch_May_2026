import json
import os

from retriever import (get_retriever,retrieve_documents,build_context)

from vector_store import (load_vector_store)

from chains import (generate_answer)


BENCHMARK_QUESTIONS = [

    "What are Amazon's business segments?",

    "Who are Amazon's primary customers?",

    "Summarize Amazon's business model.",

    "Summarize Amazon's AI strategy.",

    "Compare North America and AWS segments.",

    "What risks are discussed in the report?",

    "What will Amazon stock price be in 2027?",

    "Did Amazon guarantee future AI profits?"
]


def run_benchmark():

    vectordb = (load_vector_store())

    retriever = (get_retriever(vectordb))

    results = []

    for question in (BENCHMARK_QUESTIONS):

        docs = retrieve_documents(question,retriever)

        context = build_context(docs)

        answer = (generate_answer(question,context))

        results.append(
            {
                "question":
                question,

                "result":
                answer
            }
        )

    os.makedirs("outputs",exist_ok=True)

    with open("outputs/benchmark_results.json","w",encoding="utf-8") as file:

        json.dump(results,file,indent=2,ensure_ascii=False)

    print("\nBenchmark completed.")


if __name__ == "__main__":
    run_benchmark()