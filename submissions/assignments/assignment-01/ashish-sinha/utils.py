import json
import re
from pathlib import Path

from groq_client import call_llm


def repair_json(text):

    # remove markdown fences if present
    text = text.replace("```json", "")
    text = text.replace("```", "")

    # find first json object
    start = text.find("{")

    if start == -1:
        return text

    text = text[start:]

    # remove trailing commas
    text = re.sub(r",\s*}", "}", text)
    text = re.sub(r",\s*]", "]", text)

    # auto-close brackets/braces
    open_curly = text.count("{")
    close_curly = text.count("}")

    open_square = text.count("[")
    close_square = text.count("]")

    text += "]" * (open_square - close_square)
    text += "}" * (open_curly - close_curly)

    return text


def extract_json(response_text):

    # FIRST TRY NORMAL JSON
    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        pass

    # REPAIR BROKEN JSON
    repaired = repair_json(response_text)

    try:
        return json.loads(repaired)

    except Exception as e:

        print("\nJSON PARSE FAILED")
        print(str(e))

        return None


def save_output(filename, data):

    output_dir = Path("Outputs")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def run_case(case_name, prompt, temperature=0.2):

    raw_response = call_llm(
        prompt,
        temperature=temperature
    )

    parsed_output = extract_json(raw_response)

    result = {
        "case_name": case_name,
        "raw_response": raw_response,
        "parsed_output": parsed_output
    }

    save_output(
        f"{case_name}.json",
        result
    )

    return result