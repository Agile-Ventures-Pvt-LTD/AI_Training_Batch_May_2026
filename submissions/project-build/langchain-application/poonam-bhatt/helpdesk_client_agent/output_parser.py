import json


def safe_output(data):
    """
    Convert DB output into safe string.
    Prevents None / list / dict issues.
    """
    if data is None:
        return "No data found."

    if isinstance(data, list) and len(data) == 0:
        return "No records found."

    if isinstance(data, dict):
        return json.dumps(data, default=str)

    return str(data)


def truncate(text, max_chars=2000):
    """
    Prevents token overflow by trimming large outputs.
    """
    text = str(text)
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[TRUNCATED]"
    return text


def format_rows(rows, limit=5):
    """
    Formats DB rows into readable JSON string.
    """
    if not rows:
        return "No records found."

    rows = rows[:limit]
    return truncate(json.dumps(rows, default=str, indent=2))