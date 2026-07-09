import os
import json
from datetime import datetime
from retrievers import (build_vector_store)
from prebuilt_agent import (agent)
def initialize_vector_store():
    db_file = os.path.join("vector_store","chroma.sqlite3")
    if not os.path.exists(db_file):
        print("\nBuilding Vector Store...")
        build_vector_store()
        print("Vector Store Created")
    else:
        print("\nVector Store Loaded")
def run():
    initialize_vector_store()
    print("=" * 70)
    print("IT TROUBLESHOOTING AGENT")
    print("=" * 70)
    while True:
        query = input(
            "\nEnter Issue (exit to quit): "
        )
        if query.lower() == "exit":
            break
        try:
            result = agent.invoke( {"messages": [("user",query)]})
            print("\n" + "=" * 70)
            for message in result["messages"]:
                if hasattr(message,"content"):
                    print("\n",message.content)
        except Exception as e:
            print("\nERROR:",str(e))
def save_json_output(query, response):
    os.makedirs(
        "outputs",exist_ok=True)
    output = {
        "timestamp": str(datetime.now()),
        "user_query": query,
        "response": response
    }

    filename = "outputs/evaluation_results.json"

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nOutput saved to: {filename}"
    )


if __name__ == "__main__":
    run()