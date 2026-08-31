from prebuilt_agent import prebuilt_agent
from custom_react_agent import custom_agent
from output_formatter import save_output


print("\nCredit Card Management AI Agent")
print("1. Prebuilt ReAct Agent")
print("2. Custom ReAct Agent")

choice = input("\nChoose agent (1/2): ")

question = input("Enter your question: ")


if choice == "1":
    result = prebuilt_agent(question)

    print("\nResponse:")
    print(result)

    save_output(
        "sample_prebuilt_agent_run.txt",
        question,
        result
    )

elif choice == "2":
    result = custom_agent(question)

    print("\nResponse:")
    print(result)

    save_output(
        "sample_custom_agent_run.txt",
        question,
        result
    )

else:
    print("Invalid option selected")