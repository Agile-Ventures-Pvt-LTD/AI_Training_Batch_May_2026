from __future__ import annotations
import json
import asyncio
from pathlib import Path

from host import ask

try:
    PARENT_DIR = Path(__file__).resolve().parent
except NameError:
    PARENT_DIR = Path.cwd()

QUERIES_PATH = PARENT_DIR / "data" / "sample_queries.json"
RESULTS_JSON_PATH = PARENT_DIR / "outputs" / "mandatory_query_results.json"
RESULTS_MD_PATH = PARENT_DIR / "outputs" / "sample_run_outputs.md"


async def main() -> None:
    queries = json.load(open(QUERIES_PATH))["mandatory_queries"]

    results = []
    for q in queries:
        try:
            answer = await ask(q["query"])
            status = "PASS"
        except Exception as e:
            answer = f"ERROR: {e}"
            status = "FAIL"

        results.append({
            "query_id": q["id"],
            "user_query": q["query"],
            "final_answer": answer,
            "status": status,
        })

    RESULTS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_JSON_PATH, "w") as f:
        json.dump(results, f, indent=2)

    with open(RESULTS_MD_PATH, "w") as f:
        f.write("# Sample Run Outputs\n\n")
        for r in results:
            f.write(f"## {r['query_id']}\n\n")
            f.write(f"**User Query:**\n\n{r['user_query']}\n\n")
            f.write(f"**Final Answer:**\n\n{r['final_answer']}\n\n---\n\n")


if __name__ == "__main__":
    asyncio.run(main())