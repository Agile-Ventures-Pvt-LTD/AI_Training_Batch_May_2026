from pathlib import Path
from langchain_core.messages import HumanMessage
from prebuilt_agent import agent

OUTPUT_FILE = "outputs/sample_prebuilt_agent_run.txt"

def save_interaction(file_handle, question, answer):
    file_handle.write(f"USER:{question}")
    file_handle.write(f"ASSISTANT:{answer}")
    file_handle.flush()

def main():
    Path("outputs").mkdir(exist_ok=True)
    print("Type 'exit' to quit")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        while True:
            question = input("User: ").strip()
            if question.lower() == "exit":
                break
            if not question:
                continue
            try:
                result = agent.invoke({"messages": [HumanMessage(content=question)]})
                answer = result["messages"][-1].content
                print("Assistant:")
                print(answer)
                save_interaction(f,question,answer)

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                print(f"{error_msg}")
                save_interaction(f,question,error_msg)


if __name__ == "__main__":
    main()