import os
import sys

def main():
    print("🚀 Starting the Batch Resume Screening Pipeline with Groq...")
    
    from config import GROQ_API_KEY
    if not GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY not found in your .env file!")
        sys.exit(1)

    # Import and trigger the loop function
    from crew import run_batch_screening
    run_batch_screening()

    print("\n🎉 BATCH EXECUTION COMPLETE!")
    print("====================================================")
    print("Verify your reports under the outputs/ directory:")
    print(" - outputs/CAND-001_screening_report.json")
    print(" - outputs/CAND-002_screening_report.json")
    print(" - outputs/CAND-003_screening_report.json")
    print("====================================================")

if __name__ == "__main__":
    main()
