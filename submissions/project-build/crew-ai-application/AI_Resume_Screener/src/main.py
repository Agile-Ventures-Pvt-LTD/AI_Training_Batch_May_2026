import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

import litellm
litellm.num_retries = 6

import argparse
import time
from crew import screening_crew
from config import REQUIRED_CANDIDATES


def run_candidate(candidate_id: str):
    print(f"\nScreening {candidate_id}...")
    for attempt in range(3):
        try:
            screening_crew.kickoff(inputs={"candidate_id": candidate_id})
            print(f"Done. Report saved")
            return
        except litellm.RateLimitError:
            if attempt < 2:
                wait = 60
                print(f"Rate limit hit (attempt {attempt + 1}/3), waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"Failed for {candidate_id}: rate limit exceeded after 3 attempts")
        except Exception as e:
            print(f"Failed for {candidate_id}: {e}")
            return


def run_sample_screening():
    for candidate_id in REQUIRED_CANDIDATES:
        run_candidate(candidate_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-id", type=str)
    parser.add_argument("--run-sample-screening", action="store_true")
    args = parser.parse_args()

    if args.candidate_id:
        run_candidate(args.candidate_id)
    elif args.run_sample_screening:
        run_sample_screening()
    else:
        print("Usage: python main.py --candidate-id CAND-001")
        print("       python main.py --run-sample-screening")
