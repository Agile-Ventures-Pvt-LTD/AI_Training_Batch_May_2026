import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prebuilt_agent import run_prebuilt_agent


MANDATORY_TEST_QUESTIONS = [
    "Amit says VPN times out after MFA approval. What should we check and what is the next action?",
    "Priya's laptop is very slow after startup. Diagnose the likely issue.",
    "David cannot login and password reset email is not received. What should be done?",
    "Sara's VPN disconnects frequently. What is the likely reason?",
    "Outlook is not syncing for Emily but webmail works. What is the next step?",
    "Which active known incidents may affect VPN users?",
    "Create a ticket summary for Rahul's laptop performance issue.",
    "My email is slow. Fix it.",
]


def run_benchmark():
    print("\n" + "=" * 60)
    print("BENCHMARK - 8 MANDATORY TEST QUESTIONS")
    print("=" * 60)

    results = []
    for i, question in enumerate(MANDATORY_TEST_QUESTIONS, 1):
        print(f"\nQuestion {i}/{len(MANDATORY_TEST_QUESTIONS)}: {question}")
        try:
            response = run_prebuilt_agent(question, verbose=True)
            results.append({"question": question, "status": "success", "response": response})
        except Exception as e:
            print(f"Error: {e}")
            results.append({"question": question, "status": "error", "error": str(e)})

    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", "evaluation_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nBenchmark complete. Results saved to {output_path}")
    return results


def interactive_mode():
    print("\n" + "=" * 60)
    print("IT TROUBLESHOOTING AGENT")
    print("Type 'quit' to exit. Type 'benchmark' to run all 8 test questions.")
    print("=" * 60)

    while True:
        try:
            query = input("\nEnter IT support query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit"):
            print("Goodbye.")
            break

        if query.lower() == "benchmark":
            run_benchmark()
            continue

        try:
            run_prebuilt_agent(query, verbose=True)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--benchmark":
        run_benchmark()
    elif len(sys.argv) > 1 and sys.argv[1] == "--query":
        run_prebuilt_agent(" ".join(sys.argv[2:]), verbose=True)
    else:
        interactive_mode()
