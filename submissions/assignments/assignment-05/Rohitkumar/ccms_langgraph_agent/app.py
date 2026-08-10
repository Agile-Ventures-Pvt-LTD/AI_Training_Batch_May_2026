
import sys
from output_formatter import format_and_print


def run_prebuilt_agent():
    """Run the pre-built ReAct agent interactively and output structured responses."""
    from prebuilt_agent import agent
    print("\n=== Pre-built ReAct Agent ===")
    print("Type 'exit' to quit.\n")
    while True:
        question = input("User: ").strip()
        if question.lower() == "exit":
            break
        response = agent.invoke({"messages": [("user", question)]})
        format_and_print(question, response, "prebuilt_react_agent")


def run_custom_agent():
    """Run the custom LangGraph ReAct agent interactively and output structured responses."""
    from custom_react_agent import custom_agent
    print("\n=== Custom LangGraph ReAct Agent ===")
    print("Type 'exit' to quit.\n")
    while True:
        question = input("User: ").strip()
        if question.lower() == "exit":
            break
        response = custom_agent.invoke({"messages": [("user", question)]})
        format_and_print(question, response, "custom_react_agent")


def main():
    print("=" * 60)
    print("  Credit Card Management System - AI Agent")
    print("  Using LangGraph, Groq, and SQLite")
    print("=" * 60)

    print("\nChoose an option:")
    print("  1) Pre-built ReAct Agent")
    print("  2) Custom LangGraph ReAct Agent")
    print("  3) Exit")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1":
        run_prebuilt_agent()
    elif choice == "2":
        run_custom_agent()
    else:
        print("Exiting. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()