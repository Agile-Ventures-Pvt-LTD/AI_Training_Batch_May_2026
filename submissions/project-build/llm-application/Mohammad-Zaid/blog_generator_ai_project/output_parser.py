
import json
import os


def parse_json_response(response_text):
    try:
        return json.loads(response_text)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by model: {e}"
        )

def save_output(output_folder="outputs", output_file="sample_blog_output.json"):

    file_path = os.path.join(
        output_folder,
        output_file
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(f, indent=4, ensure_ascii=False)
    
    return file_path