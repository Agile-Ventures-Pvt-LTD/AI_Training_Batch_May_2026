try:
    import json
    from pathlib import Path
    from tools.init import tools
    from utils.logger import append_to_json_log
    from queries_for_test import TEST_CASES
except ModuleNotFoundError as m:
    print(f"Error: {m}")

def run_tool_tests():

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "test_tools_output.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([], f)

    for tool in tools:

        print(f"Testing {tool.name}")

        try:

            args = TEST_CASES.get(
                tool.name,
                {}
            )

            result = tool.invoke(args)

            log_record = {
                "tool_name": tool.name,
                "status": "PASS",
                "input": args,
                "output": result
            }

        except Exception as e:

            log_record = {
                "tool_name": tool.name,
                "status": "FAIL",
                "input": TEST_CASES.get(
                    tool.name,
                    {}
                ),
                "error": str(e)
            }

        append_to_json_log(
            log_record,
            str(output_file)
        )

    print(
        f"\nResults written to {output_file}"
    )


if __name__ == "__main__":
    run_tool_tests()