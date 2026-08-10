import argparse
import sys
from src.crew import screen_candidate, run_sample_screening, run_all_screening


def main():
    parser = argparse.ArgumentParser(description="AI Resume Screening and Interview Planning Crew")
    parser.add_argument("--candidate-id", type=str, help="Candidate ID to screen (e.g., CAND-001)")
    parser.add_argument("--run-sample-screening", action="store_true", help="Run screening for CAND-001, CAND-002, CAND-003")
    parser.add_argument("--run-all", action="store_true", help="Run screening for all 5 candidates")

    args = parser.parse_args()

    if args.candidate_id:
        result = screen_candidate(args.candidate_id)
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)
        print(f"Candidate: {result['candidate_id']}")
        print(f"Report saved: {result.get('report_json', 'N/A')}")
        print(f"Status: {result['status']}")
    elif args.run_sample_screening:
        results = run_sample_screening()
        print("\n=== Sample Screening Results ===")
        for r in results:
            if "error" in r:
                print(f"  {r.get('candidate_id', '?')}: Error - {r['error']}")
            else:
                print(f"  {r['candidate_id']}: Status - {r['status']}")
    elif args.run_all:
        results = run_all_screening()
        print("\n=== All Candidates Screening Results ===")
        for r in results:
            if "error" in r:
                print(f"  {r.get('candidate_id', '?')}: Error - {r['error']}")
            else:
                print(f"  {r['candidate_id']}: Status - {r['status']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()