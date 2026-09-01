import json
from prebuilt_agent import run_prebuilt_agent
import output_parser

def run_query(query):
    res=run_prebuilt_agent(query)
    response=res.get("final_response","")
    try:
            parsed = output_parser.parse_json(response)
            print(json.dumps(parsed, indent=2))
    except Exception:
            print(response)


print("Helloo! This is IT Troubleshooting agent, to exit the loop type 'exit'")
while True:
        try:
                user_input = input("\nEnter your query: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit"]:
                    print("Thank you!")
                    break
                run_query(user_input)
        except (KeyboardInterrupt):
                print("\nThank you!")
                break