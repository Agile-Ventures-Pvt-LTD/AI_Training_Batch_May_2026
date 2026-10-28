from chains import call_assistant

while True: 
    question = input("\nAsk: ") 
    if question.lower() in ["quit", "exit", "stop"]: 
        break 
    
    response = call_assistant(question) 
    print("\nAnswer:") 
    print(response)

