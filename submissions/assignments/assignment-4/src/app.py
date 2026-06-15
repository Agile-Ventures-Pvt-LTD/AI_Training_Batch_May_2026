from dotenv import load_dotenv
load_dotenv()

from agent import answer

if __name__ == "__main__":
    print("E-Commerce Agent ready. Type 'exit' to quit.\n")
    while True:
        query = input("Ask a question (or 'exit'): ").strip()
        if query.lower() == "exit":
            break
        if not query:
            continue
        print(answer(query))
        print()
