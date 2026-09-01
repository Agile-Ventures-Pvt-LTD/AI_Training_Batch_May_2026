import os
import argparse
import logging
import json
from src.config import OUTPUT_PATH
from src.crew import run_screening_for_candidate

log_file_path = os.path.join(OUTPUT_PATH, "execution_log.txt")
os.makedirs(OUTPUT_PATH, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(log_file_path, encoding="utf-8"), logging.StreamHandler()]
)
logger = logging.getLogger("ResumeScreening&InterviewPlanning")

def run_single(candidate_id):
    logger.info(f"Starting screening for: {candidate_id}")
    try:
        report = run_screening_for_candidate(candidate_id)
        if report:
            logger.info(f"Successfully screened.")
            print(json.dumps(report, indent=2))
        else:
            logger.error(f"Failed")
    except Exception as e:
        logger.error(f"Error screening {candidate_id}: {str(e)}")

def run_sample():
    candidates = ["CAND-001", "CAND-002", "CAND-003"]
    logger.info(f"Starting screening for: {candidates}")
    for cand_id in candidates:
       
        run_screening_for_candidate(cand_id)
        logger.info(f"Completed screening for {cand_id}.")
       

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--candidate-id", type=str)
    group.add_argument("--run-sample-screening", action="store_true")
    
    args = parser.parse_args()
    
    if args.candidate_id:
        run_single(args.candidate_id)
    elif args.run_sample_screening:
        run_sample()

if __name__ == "__main__":
    main()
