import os
import json

def output_writer(data, filename: str):
    try:
        os.makedirs("outputs", exist_ok=True)
        file_path = os.path.join("outputs", filename)

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        if isinstance(data, list):
            existing_data.extend(data)
        else:
            existing_data.append(data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        print("File saved successfully\n")

    except Exception as e:
        print(f"Error while saving file: {e}")
