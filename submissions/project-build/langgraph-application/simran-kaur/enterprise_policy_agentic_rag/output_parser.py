import json
import os

# File path for JSON file
file_path = "outputs/sample_custom_agent_run.json"

def output_formatter_func(output):
    try:
        # --- WRITE (Serialize Python object to JSON file) ---
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(output, json_file, indent=4)  # indent for pretty formatting
        print(f"Data successfully written to {file_path}")

        # --- READ (Parse JSON file into Python object) ---
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as json_file:
                parsed_data = json.load(json_file)  # Convert JSON to Python dict
            print("Parsed JSON data:", parsed_data)
        else:
            print(f"File {file_path} not found.")

    except (OSError, json.JSONDecodeError) as e:
        print(f"Error handling JSON file: {e}")