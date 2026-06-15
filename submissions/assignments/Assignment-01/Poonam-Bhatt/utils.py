import json
import re
import os


def save_output(filename, data):

    os.makedirs(
        os.path.dirname(filename),
        exist_ok=True
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(data)

    print(f"Saved to {filename}")


def parse_json(response_text):
    try:
        cleaned = response_text.strip()

        cleaned = re.sub(r"```json|```", "", cleaned, flags=re.IGNORECASE).strip()

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No JSON found")

        cleaned = cleaned[start:end+1]

        return json.loads(cleaned)

    except Exception as e:
        print("JSON Parsing Failed:", e)
        return None