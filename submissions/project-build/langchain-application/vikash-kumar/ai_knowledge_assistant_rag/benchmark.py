import json
from datetime import datetime

from embeddings import get_embedding_model

from vector_store import load_vector_store

from retriever import (get_retriever,retrieve_context)

from chains import (classify_query,generate_answer)

from output_parser import build_sources


BENCHMARK_QUESTIONS = [
     " What are Tesla’s main business segments described in the filings?",
     " What risks are mentioned related to manufacturing or supply chain?",
     "Summarize the key risk factors in 5 bullet points.",
     " What does the document say about automotive revenue or energy generation and storage?",
     " Compare Tesla’s automotive business and energy business based on the provided documents.",
     "What legal or regulatory risks are mentioned?",
     " What will Tesla’s stock price be next year?",
     "Did the document say Tesla guarantees future profitability from AI products?"
]


def run_benchmark():

    print("\nLoading Vector Store")

    embedding_model = get_embedding_model()

    vector_db = load_vector_store(embedding_model)

    retriever = get_retriever(vector_db)

    results = []

    for id, question in enumerate(BENCHMARK_QUESTIONS,start=1):

        print(f"\n[{id}/{len(BENCHMARK_QUESTIONS)}]")

        print(f"Question: {question}")

        try:
            query_type = classify_query(question)

            docs = retrieve_context(retriever,question)

            answer = generate_answer(question,docs)

            sources = build_sources(docs)

            result = {
                "question": question,
                "query_type":
                    query_type.content,
                "answer":
                    answer.content,
                "sources":
                    sources,
                "timestamp":
                    datetime.now().isoformat()
            }

            results.append(result)

            print("Completed")

        except Exception as e:

            print(f"Failed: {e}")

            results.append(
                {
                    "question": question,
                    "error": str(e)
                }
            )

    with open("outputs/benchmark_results.json","w",encoding="utf-8") as f:
            json.dump(
            results,f,
            indent=4,
            ensure_ascii=False)

    print("\nBenchmark completed.")

    print("Results saved to outputs/benchmark_results.json")


if __name__ == "__main__":

    run_benchmark()