try:
    import json
    from datetime import datetime
    from pathlib import Path
    from agents.prebuilt_agent import ask_agent, get_tools_used
    from utils.response_formatter import format_agent_response
    from utils.logger import append_to_json_log
    from queries_for_test import TEST_QUERIES
except ModuleNotFoundError as m:
    print(f"Error: {m}")



def run_tests():

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "test_agent_output.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([], f)

    for query in TEST_QUERIES:

        print(f"Running: {query}")

        try:

            response = ask_agent(query)

            formatted_response = format_agent_response(
                user_question=query,
                response=response
            )

        except Exception as e:

            formatted_response = {
                "user_question": query,
                "implementation_choice": "prebuilt_react_agent",
                "tools_used": [],
                "records_found": 0,
                "answer": "",
                "sensitive_data_masked": True,
                "limitations": [str(e)]
            }

        append_to_json_log(
            formatted_response,
            str(output_file)
        )


    print(f"\nResults written to:")
    print(f" - {output_file}")

if __name__ == "__main__":
    run_tests()