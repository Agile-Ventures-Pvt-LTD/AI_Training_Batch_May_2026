import json
import re


def repair_json(text: str):

    text = text.strip()

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:
        return match.group()

    return text


def parse_json(text: str):

    try:
        return json.loads(text)

    except Exception:

        repaired = repair_json(text)

        try:
            return json.loads(repaired)

        except Exception:
            raise ValueError(
                f"Unable to parse JSON:\n{repaired}"
            )


