from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Any

from prebuilt_agent import handle_query
from prompts import DEFAULT_SAMPLES, QUERY_PROMPT, EVALUATION_FILENAME

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / EVALUATION_FILENAME


def load_existing_evaluation() -> list[dict[str, Any]]:
    if not OUTPUT_FILE.exists():
        return []

    try:
        raw = OUTPUT_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        data = json.loads(raw)
        if isinstance(data, list):
            return data
    except Exception:
        pass

    return []


def save_output(result: dict) -> Path:
    data = load_existing_evaluation()
    data.append(result)
    OUTPUT_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return OUTPUT_FILE


def run_query(query: str, user_identifier: str | None = None) -> dict:
    return handle_query(query, user_identifier=user_identifier)


def main() -> None:
    parser = argparse.ArgumentParser(description="IT Troubleshooting Agent CLI")
    parser.add_argument("--query", "-q", help="User query to diagnose", required=False)
    parser.add_argument("--user", "-u", help="User identifier (user_id or email)", required=False)
    parser.add_argument("--queries", help="Provide multiple queries (space-separated)", nargs='+', required=False)
    parser.add_argument("--batch-file", help="Path to newline-separated queries file", required=False)
    parser.add_argument("--sample", "-s", help="Run sample question number (1-8)", type=int, required=False)
    args = parser.parse_args()
    # Determine queries to run: single, sample, multiple, or batch-file
    queries: list[tuple[str, int | None]] = []
    if args.queries:
        for q in args.queries:
            queries.append((q, None))
    elif args.batch_file:
        p = Path(args.batch_file)
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    queries.append((line, None))
        else:
            print(f"Batch file not found: {p}")
            return
    elif args.query:
        queries.append((args.query, None))
    elif args.sample is not None:
        index = max(1, min(len(DEFAULT_SAMPLES), args.sample)) - 1
        queries.append((DEFAULT_SAMPLES[index], args.sample))
    else:
        # interactive mode: allow multiple queries until empty line
        print("Enter queries: ")
        while True:
            try:
                line = input().strip()
            except EOFError:
                break
            if not line:
                break
            queries.append((line, None))

    if not queries:
        print("No queries provided.")
        return

    # Run all queries and collect results
    batch_results = []
    for q, sid in queries:
        res = run_query(q, user_identifier=args.user)
        batch_results.append({
            "timestamp": datetime.now().isoformat(),
            "query": q,
            "user_identifier": args.user,
            "sample_id": sid,
            "result": res,
        })

    evaluation = {
        "timestamp": datetime.now().isoformat(),
        "source": "app-batch",
        "count": len(batch_results),
        "results": batch_results,
    }

    saved_path = save_output(evaluation)
    print(json.dumps(evaluation, indent=2))
    print(f"Saved evaluation entry to: {saved_path}")


if __name__ == "__main__":
    main()
