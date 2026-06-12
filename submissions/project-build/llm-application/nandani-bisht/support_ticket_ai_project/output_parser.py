import json
def parse_json_response(text: str) -> dict:
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Empty model response.')

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        candidate = _extract_json_object(text)
        if candidate is None:
            raise ValueError('Unable to parse JSON from model response.')
        return json.loads(candidate)


def _extract_json_object(text: str) -> str | None:
    start = None
    depth = 0
    in_string = False
    escape = False

    for index, char in enumerate(text):
        if char == '"' and not escape:
            in_string = not in_string
        if char == '\\' and not escape:
            escape = True
            continue
        escape = False

        if not in_string:
            if char == '{':
                if start is None:
                    start = index
                depth += 1
            elif char == '}':
                depth -= 1
                if start is not None and depth == 0:
                    return text[start:index + 1]

    return None
