# from agents import run_agent

# def main():
#     print("Type your query below (type 'exit' to stop)\n")

#     while True:
#         user_input = input("User: ")

#         if user_input.lower() in ["exit", "quit"]:
#             print("Exiting Agent...")
#             break

#         response = run_agent(user_input)

#         print("\n--- RESPONSE ---")
#         print(response)
#         print("\n-----------------\n")


# if __name__ == "__main__":
#     main()

from agents import run_agent
import os
from datetime import datetime

output_file = "outputs/sample_agent_run.txt"

def save_output(user_input, response):
    os.makedirs("outputs", exist_ok=True)

    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n" + "="*60 + "\n")
        f.write(f"TIME: {datetime.now()}\n")
        f.write(f"USER: {user_input}\n")
        f.write(f"RESPONSE:\n{response}\n")


def main():
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = run_agent(user_input)
        print("\nFINAL OUTPUT:\n", response)
        save_output(user_input, response)


if __name__ == "__main__":
    main()