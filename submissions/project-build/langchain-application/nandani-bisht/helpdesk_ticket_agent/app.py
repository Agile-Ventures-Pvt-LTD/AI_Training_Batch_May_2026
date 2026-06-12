import json
from pathlib import Path
from agent import run_agent
from output_formatter import (
    format_response,
    format_error
)


OUTPUT_DIR = Path("outputs")

OUTPUT_DIR.mkdir(
    exist_ok=True
)
def save_outputs(
    user_input,
    result,
    formatted_output
):
    """
    Save evaluation artifacts.
    """

    sample_file = (
        OUTPUT_DIR
        /
        "sample_agent_run.txt"
    )

    sample_file.write_text(
        formatted_output,
        encoding="utf-8"
    )

    evaluation = {

        "user_input":
        user_input,

        "response":
        result["response"],

        "tools":
        result["tools"]
    }

    with open(
        OUTPUT_DIR
        /
        "evaluation_outputs.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evaluation,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    print(
        "\nAI Helpdesk Ticket Agent"
    )
    print(
        "Type exit to stop\n"
    )

    while True:

        try:

            user_input = input(
                "Ask: "
            )

            if (
                user_input
                .lower()
                ==
                "exit"
            ):

                print(
                    "\nSession ended."
                )

                break

            result = run_agent(
                user_input
            )

            formatted = format_response(
                result["response"],
                result["tools"]
            )

            print(
                formatted
            )

            save_outputs(
                user_input,
                result,
                formatted
            )

        except Exception as e:

            print(
                format_error(
                    e
                )
            )


if __name__ == "__main__":

    main()
