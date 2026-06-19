import os
from loaders import load_kb_documents
from retrievers import create_retriever
from config import KB_PATH, VECTOR_STORE_PATH
from prebuilt_agent import build_agent
from output_parser import save_output
import tools
import json


def main():
    print("Setting up system...")

    if not os.path.exists(VECTOR_STORE_PATH) or not os.listdir(VECTOR_STORE_PATH):
        print("Loading knowledge base (first time)...")
        docs = load_kb_documents(KB_PATH)
    else:
        print("Skipping Knowledge Base loading (already indexed)")
        docs = []

    print("Preparing retriever...")
    global retriever
    retriever = create_retriever(docs)

    tools.set_retriever(retriever)

    print("Starting agent...")
    agent = build_agent()

    print("\nIT Troubleshooting Agent Ready")
    print("Type 'exit' to quit\n")

    while True:
        query = input("User: ").strip()

        if query.lower() == "exit":
            break

        try:
            print("Processing...")   

            response = agent.invoke({
                "messages": [("user", query)]
            })

            final_answer = response["messages"][-1].content

            # print("\nAgent:", final_answer)
            
            try:
                parsed = json.loads(final_answer)
                print("\nAgent (structured):")
                print(json.dumps(parsed, indent=2))
            except:
                print("\nAgent:", final_answer)

            print("\n---")

            save_output(query, final_answer)

        except Exception as e:
            print("Error:", str(e))
            print("---")


if __name__ == "__main__":
    main()