import os
import csv
import sys
from crew import build_screening_crew
from output_writer import parse_and_save_report

def run_project_pipeline():
    print("AI RESUME SCREENING")
    
    DATASET_PATH = "data/p004_resume_screening_crew_dataset"
    OUTPUT_PATH = "outputs"
    JD_PATH = os.path.join(DATASET_PATH, "job_description", "jd_ai_engineer.md")
    RESUMES_DIR = os.path.join(DATASET_PATH, "resumes")
    CSV_PATH = os.path.join(DATASET_PATH, "metadata", "candidate_index.csv")
    
    if not os.path.exists(CSV_PATH):
        print(f"[-] Error: Index file not found at {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    candidates = []
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("candidate_id"):
                candidates.append(row["candidate_id"].strip())
                
    screening_crew = build_screening_crew()
    
    for candidate_id in candidates:
        print(f"\n[>>>] Processing Candidate ID: {candidate_id}")
        
        inputs = {
            "jd_path": JD_PATH,
            "candidate_id": candidate_id,
            "resumes_dir": RESUMES_DIR  
        }
        
        try:
            crew_output = screening_crew.kickoff(inputs=inputs)
            raw_result_data = {
                "raw": crew_output.raw,
                "json_dict": crew_output.json_dict if hasattr(crew_output, "json_dict") else None
            }
            parse_and_save_report(candidate_id, raw_result_data, OUTPUT_PATH)
        except Exception as e:
            print(f"[-] Pipeline failed for {candidate_id}: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    run_project_pipeline()
