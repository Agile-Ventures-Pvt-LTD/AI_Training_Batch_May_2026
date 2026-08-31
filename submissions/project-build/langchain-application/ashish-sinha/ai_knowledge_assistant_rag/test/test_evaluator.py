import json
import os

from vector_store import load_vector_store
from chains import RAGChains

Benchmark_Question = [
    "What are Tesla's main business segments described in the filings?",
    "What risks are mentioned related to manufacturing or supply chain?",
    "Summarize the key risk factors in 5 bullet points.",
    "What does the document say about automotive revenue or energy generation and storage?",
    "Compare Tesla's automotive business and energy business based on the provided documents.",
    "What legal or regulatory risks are mentioned?",
    "What will Tesla's stock price be next year?",
    "Did the document say Tesla guarantees future profitability from AI products?"
]


def run_evaluation():

    os.makedirs("outputs", exist_ok=True)

    vector_store = load_vector_store()

    rag = RAGChains(vector_store)

    output_file = "outputs/benchmark_results.json"

    open(output_file, "w").close()

    for idx, question in enumerate( Benchmark_Question,start=1):

        print(f"Questions {idx}")
        print(question)

        response = rag.generate_answer(question)

        print("Answer:")
        print(response)

        record = {
            "question": question,
            "response": response
        }

        with open(output_file,"a",encoding="utf-8") as f:

            f.write( json.dumps(record) + "\n")

    print(f"\nBenchmark results saved to: {output_file}")


if __name__ == "__main__":
    run_evaluation()