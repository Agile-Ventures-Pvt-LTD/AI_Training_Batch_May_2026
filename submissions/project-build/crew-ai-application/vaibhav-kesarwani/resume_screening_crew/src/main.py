from src.crew import resume_screening_crew

while True: 
    question = input("\nAsk: ") 
    if question.lower() in ["quit", "exit", "stop"]: 
        break 
    
    result = resume_screening_crew.kickoff({"user_query" : question})

    print(result)