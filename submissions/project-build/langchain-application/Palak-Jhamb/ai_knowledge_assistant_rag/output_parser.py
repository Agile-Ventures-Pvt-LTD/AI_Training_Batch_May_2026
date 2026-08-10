import json
from pathlib import Path
 
 
def merge_json_files(input_folder="outputs", output_file="merged_output.json"):
    input_path = Path(input_folder)
 
    if not input_path.exists():
        print(f"Folder '{input_folder}' does not exist.")
        return
 
    merged_data = []
 
    json_files = list(input_path.glob("*.json"))
 
    if not json_files:
        print(f"No JSON files found in '{input_folder}'.")
        return
 
    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                merged_data.append(data)
 
        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
 
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)
 
    print(f"Merged {len(json_files)} files into '{output_file}'")
 
 
if __name__ == "__main__":
    merge_json_files(
        input_folder="output",          # Folder containing JSON files
        output_file="merged_output.json"
    )