# main.py

    
from dotenv import load_dotenv
load_dotenv()

import os
from config import GROQ_API_KEY
from call_crew import run_screening_crew 

if not GROQ_API_KEY:
    raise ValueError("Key not set")
else:
    print("API key set\n")

def main():
    print("=== AI Resume Screening System ===")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("Enter Candidate ID (EX: CAND-001): ").strip()
        
        if user_input.lower() == 'quit':
            print("Exiting Screening AI. !!") 
            break
            
        if not user_input:
            print("Error: Input cannot be empty. Try again with valid Input.\n")
            continue
   
        if not user_input.startswith("CAND-") or len(user_input) < 8:
            print("Error: Invalid Candidate ID format. Please input like: 'CAND-001'.\n")
            continue
            
        print(f"\n--- Starting screening for {user_input} ---")
        
        try:
            crew = run_screening_crew(candidate_id=user_input)
            result = crew.kickoff(inputs={"candidate_id": user_input})
            
            print(f"\n--- Successfully finished screening for {user_input} ---")
            print(f"Crew AI Output:\n{result}\n")
            
        except Exception as e:
            print(f"\nError!! while screening {user_input}.")
            print(f"Details: {e}\n")

if __name__ == "__main__":
    main()