import sys
import json
import logging
import argparse
from pathlib import Path

import config
import loaders
import chunking
import retrievers
from prebuilt_agent import run_agent

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


def build_index():
    docs = loaders.load_policy_documents()
    print(f"Loaded {len(docs)} pages from {config.POLICY_DATA_PATH}")
    chunks = chunking.chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")
    retrievers.build_vectorstore(chunks)
    print(f"Index saved to {config.VECTOR_STORE_PATH}")


def show_response(response: dict):
    print("\n" + "="*60)
    print(response.get("answer", "No answer."))

    for point in response.get("policy_basis", []):
        print(f"  - {point}")

    for src in response.get("sources", []):
        if not isinstance(src, dict):
            print(f"\n  {src}")
            continue
        snippet = src.get("snippet", "")[:100]
        print(f"\n  [{src.get('policy_domain')}] {src.get('source_file')} | {src.get('chunk_id')}")
        if snippet:
            print(f"  \"{snippet}\"")

    print(f"\nConfidence : {response.get('confidence', '-')}")
    print(f"Status     : {response.get('answerability', '-')}")
    if response.get("recommended_next_step"):
        print(f"Next step  : {response['recommended_next_step']}")
    print("="*60)


def chat():
    print("Policy Assistant ready. Type 'exit' to quit.\n")
    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            break
        show_response(run_agent(q))


def run_batch(input_file: str, output_file: str):
    questions = [l.strip() for l in open(input_file) if l.strip()]
    results = []
    for i, q in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] {q}")
        resp = run_agent(q)
        show_response(resp)
        results.append({"question": q, "response": resp})

    out = Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(results, open(out, "w"), indent=2)
    print(f"\nResults saved to {output_file}")


def check_index():
    store = Path(config.VECTOR_STORE_PATH)
    if not store.exists() or not any(store.iterdir()):
        print("Run 'python app.py index' first.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Enterprise Policy Assistant")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("index")

    chat_p = sub.add_parser("chat")
    chat_p.add_argument("-q", "--question")
    chat_p.add_argument("-o", "--output")

    batch_p = sub.add_parser("batch")
    batch_p.add_argument("-i", "--input", required=True)
    batch_p.add_argument("-o", "--output", default="outputs/evaluation_results.json")

    args = parser.parse_args()

    if args.cmd == "index":
        build_index()
    elif args.cmd == "chat":
        check_index()
        if args.question:
            show_response(run_agent(args.question))
            if args.output:
                Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                json.dump({"question": args.question, "response": run_agent(args.question)},
                          open(args.output, "w"), indent=2)
        else:
            chat()
    elif args.cmd == "batch":
        check_index()
        run_batch(args.input, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    