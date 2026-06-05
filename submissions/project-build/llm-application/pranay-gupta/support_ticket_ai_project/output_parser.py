import json
import os
import re

OUTPUT_FOLDER = "Outputs"


def clean_json_text(response: str) -> str:
    
    text = response.strip()
    text = re.sub(r'```(?:json)?\s*', '', text, flags=re.IGNORECASE)
    text = text.replace('```', '').strip()
    return text


def parse_json_response(response: str) -> dict:
    
    clean_response = clean_json_text(response)

    try:
        return json.loads(clean_response)
    except json.JSONDecodeError:
        json_match = re.search(r'(\{(?:.|\n)*\}|\[(?:.|\n)*\])', clean_response, re.S)
        if json_match:
            json_string = json_match.group(1)
            return json.loads(json_string)
        
        raise ValueError("Could not find valid JSON in the response")


def save_json_output(response: str, filename: str = "sample_ticket_output.json", output_folder: str = OUTPUT_FOLDER) -> str:

    os.makedirs(output_folder, exist_ok=True)
    
    data = parse_json_response(response)
    
    file_path = os.path.join(output_folder, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return file_path
