import os
import json

def report_writers(data, filename: str):
    try:
        os.makedirs("outputs", exist_ok=True)

        file_path = os.path.join("outputs", filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("File save successfully")

    except Exception as e:
        print(f"Error while saving file : {e}")