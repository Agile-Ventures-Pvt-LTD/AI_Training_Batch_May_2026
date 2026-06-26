import argparse
import sys
from crew import create_screening_crew

def run_screening(candidate_id: str):
    jd_path = "job_description/jd_ai_engineer.md"
    print(f"Initiating screening pipeline for {candidate_id}...")
    crew = create_screening_crew(jd_path, candidate_id)
    result = crew.kickoff()
    print(f"Screening complete for {candidate_id}.")
    return result

def run_sample_screening():
    target_candidates = ["CAND-001", "CAND-002", "CAND-003", "CAND-004", "CAND-005"]
    for cid in target_candidates:
        run_screening(cid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Resume Screening Crew")
    parser.add_argument("--candidate-id", type=str, help="Screen a specific candidate")
    parser.add_argument("--run-sample-screening", action="store_true", help="Screen all 5 sample candidates")
    
    args = parser.parse_args()
    
    if args.candidate_id:
        run_screening(args.candidate_id)
    elif args.run_sample_screening:
        run_sample_screening()
    else:
        parser.print_help()
        sys.exit(1)