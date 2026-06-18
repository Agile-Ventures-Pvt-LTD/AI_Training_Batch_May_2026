import sys
from output_formatter import output_format


def run_prebuilt():
    from prebuilt_agent import agent

    OUTPUT_FILE = "outputs/sample_prebuilt_agent_run.txt"
    print("CCMS AI Agent - Pre-built ReAct")

    while True:
        user_input = input("\nAsk: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye")
            break

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            }
        )

        final_response = response["messages"][-1].content
        print("\nAnswer:\n")
        print(output_format(final_response))

        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(
                f"""USER:
{user_input}
AGENT:
{final_response}

"""
            )


def run_custom():
    from custom_react_agent import custom_agent

    print("CCMS AI Agent - Custom LangGraph")

    while True:
        user_input = input("\nAsk: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye")
            break

        response = custom_agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                "plan": "",
                "reflection": "",
                "tools_used": [],
            }
        )

        final_response = response["messages"][-1].content
        print("\nAnswer:\n")
        print(output_format(final_response))

        if response.get("reflection"):
            print(f"\nReflection: {response['reflection']}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "custom":
        run_custom()
    else:
        run_prebuilt()
