import json
from datetime import datetime
from logger import log_query 
from chain import answer_question
from chunking import chunks

benchmark_questions = [

    "What are Tesla’s main business segments described in the filings?",

    "What risks are related to supply chain?",

    "Summarize key risk factors.",

    "What does the report say about AWS revenue?",

    "Compare AWS and International segment.",

    "What legal risks are mentioned?",

    "What will Tesla stock price be next year?",

]

results = []

for question in benchmark_questions:

    print(f"\nProcessing: {question}")

    response = answer_question(question)

    result = {
        "timestamp": datetime.now().isoformat(),
        "question": question,

        "answer": response["answer"],
        "answerability": response["answerability"],
        "confidence": response["confidence"],

        "retrieved_chunks": [
            {
                "chunk_id": doc.metadata.get("chunk_id"),
                "source_file": doc.metadata.get("source_file"),
                "page_number": doc.metadata.get("page"),
                "snippet": doc.page_content[:300]
            }
            for doc in response.get("retrieved_chunks", [])
        ]
    }

    results.append(result)

    log_query(result)


#save
with open("outputs/evaluation_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

print("\nEvaluation saved to outputs/benchmark_results.json")


