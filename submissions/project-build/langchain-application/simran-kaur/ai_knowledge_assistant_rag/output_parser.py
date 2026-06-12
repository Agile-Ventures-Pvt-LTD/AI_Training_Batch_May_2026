import json
import os

from app import answer

# File path for JSON file
file_path = "outputs/sample_ticket_output.json"

try:
    # --- WRITE (Serialize Python object to JSON file) ---
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(final_response, json_file, indent=4)  # indent for pretty formatting
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