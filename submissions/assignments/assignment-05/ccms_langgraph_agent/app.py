from langchain_core.messages import HumanMessage
from custom_react_agent import compiled_flow as custom_agent
from prebuilt_agent import compiled_flow as prebuilt_agent

custom_output_file = "outputs/custom_agent_run.txt"
prebuilt_output_file = "outputs/prebuilt_agent_run.txt"

def save_output(output_file, user_query, agent_response):
    with open(output_file, "a",encoding="utf-8") as f:
        f.write(f"User Query:\n{user_query}\n\n")
        f.write(f"Agent Response:\n{agent_response}\n")

def select_agent():
    print("\nChoose Agent Implementation")
    print("1. Custom ReAct Agent")
    print("2. Prebuilt ReAct Agent")
    choice = input("\nEnter choice 1/2 : ").strip()
    if choice == "2":
        return "prebuilt_react_agent", prebuilt_agent, prebuilt_output_file
    return "custom_react_agent", custom_agent, custom_output_file

def main():
    implementation, agent, output_file = select_agent()
    print("\nCCMS Customer Support Agent")
    print(f"Implementation: {implementation}")
    print("Type 'exit' to quit")
    while True:
        user_question = input("\nUser: ").strip()
        if user_question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        try:
            if implementation == "custom_react_agent":
                state = {
                    "messages": [HumanMessage(content=user_question)],
                    "user_question": user_question,
                    "implementation_choice": implementation,
                    "tools_used": []
                }
                result = agent.invoke(state)
                response = result["final_response"]
            else:
                result = agent.invoke(
                    { "messages": [HumanMessage(content=user_question)]})
                response = result["messages"][-1].content
            print("\nAgent Response:\n")
            print(response)
            save_output(output_file,user_question,str(response))
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()