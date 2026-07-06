import os
import json

def save_result(data):
    os.makedirs("outputs", exist_ok=True)
    output_file = "outputs/results.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data,f)


