from custom_react_agent import custom_agent_executor
from output_formatter import format_agent_output
import json
import os
 
def main():
    print("Credit Card Management Agent")
    print("Type 'exit' to quit.\n")
    while True:
        question = input("Ask: ")
        if question.lower() == "exit":
            break
        try:
            result = custom_agent_executor.invoke(
                {"messages": [("user", question)]})
            response = format_agent_output(question, result)
        except Exception as e:
            response = {
                "user_question": question,
                "implementation_choice": "custom_react_agent",
                "tools_used": [],
                "records_found": 0,
                "answer": f"Unable to process request: {str(e)}",
                "sensitive_data_masked": True,
                "limitations": []
            }
        print("\nResponse:")
        print(response["answer"])
        os.makedirs("outputs", exist_ok=True)
        output_file = "outputs/sample_custom_agent_run.txt"
        with open(output_file, "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"QUESTION:\n{question}\n\n")
            f.write("RESPONSE:\n")
            f.write(json.dumps(response, indent=4))
            f.write("\n")
        print(f"\noutput appended to {output_file}")
if __name__ == "__main__":
    main()