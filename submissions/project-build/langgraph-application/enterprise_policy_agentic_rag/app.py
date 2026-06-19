from loaders import load_documents
from chunking import chunk_documents
from retrievers import create_vectorstore
from graph import build_graph
from typing import Any, cast
from config import POLICY_DATA_PATH
from output_parser import save_output
from evaluator import evaluate_answer


def main():
    print("Loading documents...")
    docs = load_documents(POLICY_DATA_PATH)

    print("Chunking...")
    chunks = chunk_documents(docs)

    print("Creating vector store...")
    vectordb = create_vectorstore(chunks)

    retriever = vectordb.as_retriever()

    graph = build_graph()

    while True:
        q = input("\nAsk: ")

        if q.lower() == "exit":
            break

        result = graph.invoke({
            "question": q,
            "retriever": retriever,
            "retrieved_context": [],
            "retry_count": 0
        })

        final_answer = result["answer"]
        print("\nFINAL ANSWER:\n")
        print(final_answer)

        # sources for evaluation
        sources = final_answer.get("sources", [])

        evaluation = evaluate_answer(
            question=q,
            result=result,
            context=sources
        )

        print("\nEVALUATION SCORE:", evaluation["score"])
        print("FEEDBACK:", evaluation["feedback"])

        save_output({
            "question": q,
            "result": final_answer,
            "evaluation": evaluation
        })
if __name__ == "__main__":
    main()