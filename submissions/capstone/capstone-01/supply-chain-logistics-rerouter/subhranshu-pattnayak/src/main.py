from graph import compiled_workflow
from utils.config import OUTPUT_DIR
import os, json

def main():
    while True:
        incident = input("Enter incident: ")
        print("Initialzing agent.")
        print('=' * 60)
        result = compiled_workflow.invoke(incident)
        with open(os.path.join(OUTPUT_DIR, "reroute_advisory_report.json"), 'a', encoding="utf-8") as f:
            json.dump(result.__dict__, f)


if __name__ == "__main__":
    main()
