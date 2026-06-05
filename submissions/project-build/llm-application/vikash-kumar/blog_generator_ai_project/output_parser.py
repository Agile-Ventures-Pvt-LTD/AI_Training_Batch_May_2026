import json
import re


def extract_json(
    text: str
):

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if not match:
            raise ValueError(
                "No JSON object found."
            )

        return json.loads(
            match.group()
        )


def save_output(
    data,
    filepath="outputs/sample_blog_output.json"
):

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )