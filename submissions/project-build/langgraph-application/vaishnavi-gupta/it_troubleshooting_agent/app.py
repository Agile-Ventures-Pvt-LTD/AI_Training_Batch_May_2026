from prebuilt_agent import ask_agent

def main():

    print("\n" + "=" * 80)
    print("IT_Troubleshooting_Agent")
    print("Implementation Choice-1 : LangGraph Prebuilt ReAct Agent")
    print("=" * 80)

    while True:

        query = input("\nAsk a question (or type 'exit'): ").strip()

        if query.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        

if __name__ == "__main__":
    main()