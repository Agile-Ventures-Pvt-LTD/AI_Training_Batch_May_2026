
import os
import time
from crew import screening_crew

def run_screening_pipeline(jd_filepath: str, candidate_identifier: str):
    """This will executes the screening crew """
    print(f"Kicking Off Automated Evaluation: {candidate_identifier}")
    print(f"Target JD Document Pathway:       {jd_filepath}")
    
    screening_crew = screening_crew()
    
    inputs = {
        "jd_path": jd_filepath,
        "candidate_id": candidate_identifier
    }
    
    max_retries = 5
    delay = 11
    
    for attempt in range(max_retries):
        try:
            results = screening_crew.kickoff(inputs=inputs)
            print(f"[{candidate_identifier}]: Pipeline Compiled Successfully.")
            return results
                        
        except Exception as e:
            print(f"\n[Unexpected Framework Crash on {candidate_identifier}]: {str(e)}")
            return None

if __name__ == "__main__":
    DEFAULT_JD = "data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md"
    
    REQUIRED_CANDIDATES = ["CAND-001", "CAND-002", "CAND-003", "CAND-004","CAND-005"]
    
    print(f"Starting Batch Recruitment Process for {len(REQUIRED_CANDIDATES)} candidates...")
    for candidate in REQUIRED_CANDIDATES:
        run_screening_pipeline(jd_filepath=DEFAULT_JD, candidate_identifier=candidate)
        print("Pausing 3 seconds between candidate context thread initializations...\n")
        time.sleep(3)