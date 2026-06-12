import json
import re

def parse_json(response):

    if not response:
        raise ValueError("Empty response received")

    response = response.strip()

    response = re.sub(
        r"^```json\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(
        r"^```",
        "",
        response
    )

    response = re.sub(
        r"```$",
        "",
        response
    )

    response = response.strip()

    try:
        return json.loads(response)

    except Exception as e:

        print(response)

        raise ValueError(
            f"Invalid JSON: {e}"
        )