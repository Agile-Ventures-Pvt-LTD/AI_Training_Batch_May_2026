import json
import re
def extract_json_block(text: str):
    """
    Extract JSON from markdown code block.
    Example:
    ```json
    {...}
    ```
    Returns:
        JSON string or original text
    """
    if not text:
        return ""

    pattern = r"```json\s*(.*?)\s*```"

    match = re.search(pattern,text,re.DOTALL)
    if match:
        return match.group(1)
    return text
def safe_json_parse(text: str):
    """
    Safely parse JSON response.

    Returns:
        dict
    """
    if not text:
        return {"error": "empty_response","raw_response": ""}
    try:
        cleaned_text = (extract_json_block(text).strip())
        parsed = json.loads(cleaned_text)
        return parsed
    except json.JSONDecodeError:
        return {"error":"invalid_json","raw_response":text}
    except Exception as exc:
        return {"error":str(exc),"raw_response":text}
def is_valid_json(text: str):
    """
    Check whether text is valid JSON.
    """
    try:
        json.loads(text)
        return True
    except Exception:
        return False
def parse_or_default(text,default_value):
    """
    Return parsed JSON
    or provided default.
    """
    parsed = safe_json_parse(text)
    if parsed.get("error"):
        return default_value
    return parsed
def pretty_print_json(data):
    """
    Pretty JSON output.
    """
    return json.dumps(data,indent=4,sort_keys=True,ensure_ascii=False)
