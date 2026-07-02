import json
from pathlib import Path

OUTPUT_FILE = Path(__file__).resolve().parent.parent / "outputs" / "jira_output.json"


def save_output(output: dict):

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(output)

    with open(OUTPUT_FILE, "w") as file:
        json.dump(data, file, indent=4)