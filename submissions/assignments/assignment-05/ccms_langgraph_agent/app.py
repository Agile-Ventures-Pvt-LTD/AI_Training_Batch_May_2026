try:
    from pathlib import Path
    from agents.prebuilt_agent import ask_agent, get_tools_used
    from utils.response_formatter import format_agent_response
    from utils.logger import append_to_json_log
except ModuleNotFoundError as e:
    print(f"Error: {e}")


def main():

    print("CCMS Agent")
    print("Type 'exit' to quit.\n")

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "conversation_log.json"

    while True:

        query = input("User: ")

        if query.lower() == "exit":
            break

        try:

            response = ask_agent(query)

            answer = response["messages"][-1].content

            print("\nAssistant:")
            print(answer)

            formatted_response = format_agent_response(
                user_question=query,
                response=response
            )

            append_to_json_log(
                formatted_response,
                str(log_file)
            )

        except Exception as e:

            print(f"\nError: {e}\n")

            error_response = {
                "user_question": query,
                "implementation_choice": "prebuilt_react_agent",
                "tools_used": [],
                "records_found": 0,
                "answer": "",
                "sensitive_data_masked": True,
                "limitations": [str(e)]
            }

            append_to_json_log(
                error_response,
                str(log_file)
            )


if __name__ == "__main__":
    main()