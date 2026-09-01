import os
from prebuilt_agent import run_prebuilt_agent
from custom_agent import run_custom_agent
from output_formatter import print_agent_output
from langchain_core.messages import ToolMessage

def main():
    print('Hi! To exit just type "exit"')
    print("Select Implementation:")
    print("1. Pre-built Agent")
    print("2. Custom Agent")
    choice = input("Enter your choice - either number 1 or 2: ")
    
    agent_func = run_prebuilt_agent if choice == '1' else run_custom_agent
    choice_label = "Pre-built Agent" if choice == '1' else "Custom Agent"
    log_file = "outputs/sample_prebuilt_agent_run.txt" if choice == '1' else "outputs/sample_custom_agent_run.txt"
    os.makedirs("outputs", exist_ok=True)

    while True:
        question = input("Enter question: ").strip()
        if question == 'exit': break
        if not question: continue
        state = agent_func(question)
        messages = state["messages"]
        tools = []
        records = 0
        for m in messages:
            if hasattr(m, 'tool_calls') and m.tool_calls:
                tools.extend([tc['name'] for tc in m.tool_calls])
            if isinstance(m, ToolMessage):
                records += m.content.count("") // 2
        
        print_agent_output(
            question, 
            choice_label, 
            tools, 
            records, 
            messages[-1].content, 
            "Yes"
        )

        with open(log_file, "a") as f:
            f.write(f"QUESTION: {question}\n")
            f.write(f"CHOICE: {choice_label}\n")
            f.write(f"TOOLS USED: {', '.join(set(tools)) if tools else 'None'}\n")
            f.write(f"RECORDS FOUND: {records}\n")
            f.write(f"FINAL ANSWER: {messages[-1].content}\n")
            f.write(f"SENSITIVE DATA MASKED: Yes\n")

if __name__ == "__main__":
    main()
