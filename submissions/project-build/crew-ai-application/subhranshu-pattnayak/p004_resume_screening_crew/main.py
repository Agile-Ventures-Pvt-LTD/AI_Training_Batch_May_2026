from crew import resume_screening_crew
from config import DATASET_PATH


def main():
    print("==================================================")
    print("AI Resume Screening Crew")
    print("==================================================")
    
    candidate_id = input("Enter Candidate ID (e.g. CAND-001): ").strip().upper()
    if not candidate_id:
        candidate_id = "CAND-001"
    
    inputs = {
        "candidate_id": candidate_id,
        "job_description_path": str(
            DATASET_PATH / "job_description" / "jd_ai_engineer.md"
        )
    }
    
    try:
        result = resume_screening_crew.kickoff(inputs=inputs)
        print("\nScreening Completed Successfully!\n")
        print(result)
    
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()