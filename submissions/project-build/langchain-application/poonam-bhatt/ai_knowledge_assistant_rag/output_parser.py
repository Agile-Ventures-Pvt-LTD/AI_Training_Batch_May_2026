
import json
import time


#Benchmark output


queries = [
    "When is the amazon LEO scheduled?",
    "What is AWS and where it is used?",
    "What compliance requirements exist?"
]

results = []

for q in queries:

    start = time.time()

    # retriever.invoke(q)

    end = time.time()

    results.append(
        end - start
    )

avg_time = sum(results) / len(results)

report = {
    "total_queries": len(queries),
    "average_retrieval_time": avg_time
}

with open(
    "outputs/benchmark_results.json1",
    "w"
) as f:

    json.dump(
        report,
        f,
        indent=4
    )

print("Benchmark Complete")