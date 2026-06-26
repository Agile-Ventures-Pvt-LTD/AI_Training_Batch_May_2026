
import os
import time
from crew import create_screening_crew
from litellm import RateLimitError

def run_screening_pipeline(jd_filepath: str, candidate_identifier: str):
    """Executes the recruitment crew with strict exponential backoff handlers for Groq API."""
    print(f"Kicking Off Automated Evaluation: {candidate_identifier}")
    print(f"Target JD Document Pathway:       {jd_filepath}")
    
    screening_crew = create_screening_crew()
    
    inputs = {
        "jd_path": jd_filepath,
        "candidate_id": candidate_identifier
    }
    
    max_retries = 4
    delay = 15 
    
    for attempt in range(max_retries):
        try:
            results = screening_crew.kickoff(inputs=inputs)
            print(f"[{candidate_identifier}]: Pipeline Compiled Successfully.")
            return results
            
        except RateLimitError as e:
            if attempt == max_retries - 1:
                print(f"\n[Fatal Error]: Maximum retries exhausted for {candidate_identifier}.")
                raise e
            print(f"\n[Rate Limit Triggered on {candidate_identifier}]: Cooldown for {delay}s...")
            time.sleep(delay)
            delay *= 2 
            
        except Exception as e:
            print(f"\n[Unexpected Framework Crash on {candidate_identifier}]: {str(e)}")
            return None

if __name__ == "__main__":
    DEFAULT_JD = "data/p004_resume_screening_crew_dataset/job_description/jd_ai_engineer.md"
    
    REQUIRED_CANDIDATES = ["CAND-001", "CAND-002", "CAND-003"]
    
    print(f"Starting Batch Recruitment Process for {len(REQUIRED_CANDIDATES)} candidates...")
    for candidate in REQUIRED_CANDIDATES:
        run_screening_pipeline(jd_filepath=DEFAULT_JD, candidate_identifier=candidate)
        print("Pausing 5 seconds between candidate context thread initializations...\n")
        time.sleep(5)
