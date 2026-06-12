import os
import uuid
from agent import get_agent
from memory import log_convo_turn
from output_formatter import formating_agent_response
import config

def main():
    if not os.path.exists(config.DB_PATH):
        print(f"Error: DB not found at {config.DB_PATH}.")
        return

    os.makedirs("outputs", exist_ok=True)
    log_file_path = "outputs/sample_agent_run.txt"


    agent = get_agent()
    session_id = f"session_{str(uuid.uuid4())[:6]}"

    while True:
        user_input = input("User: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        if not user_input.strip():
            continue

        
        
        try:
            contextual_input = f"[Session ID: {session_id}]\n{user_input}"
            inputs = {"messages": [("user", contextual_input)]}
            
            result = agent.invoke(inputs)
            final_msg = result["messages"][-1].content
            tools_used = [msg.name for msg in result["messages"] if hasattr(msg, "name") and msg.type == "tool"]
            
            formatted_output = formating_agent_response(user_input, final_msg, tools_used)
            
            print(formatted_output)

            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write(formatted_output)

            log_convo_turn(session_id, user_input, final_msg, tools_used)

        except Exception as e:
            print(f"\nAgent crashed or encountered an error: {e}\n")

if __name__ == "__main__":
    main()