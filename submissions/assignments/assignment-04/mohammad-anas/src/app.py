import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.modern_agent import run_modern_agent
from src.agents.legacy_agent import run_legacy_agent

def main():
    print("Welcome to the E-Commerce AI Agent!")
    print("1. Run Modern Agent (LangChain >= 1.0)")
    print("2. Run Legacy Agent (LangChain < 1.0)")
    print("3. Exit")
    
    choice = input("Select an option (1/2/3): ")
    
    if choice in ['1', '2']:
        query = input("\nEnter your business question: ")
        
        if choice == '1':
            print("\n--- Running Modern Agent ---")
            run_modern_agent(query)
        elif choice == '2':
            print("\n--- Running Legacy Agent ---")
            run_legacy_agent(query)
            
    elif choice == '3':
        print("Exiting...")
        sys.exit()
    else:
        print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()