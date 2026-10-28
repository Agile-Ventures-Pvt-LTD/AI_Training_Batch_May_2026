import os
import json
from groq_client import call_groq
from prompts import output_system, output_user_template

def output_schema(user_request : str, agent_response):
    AGENT_RUN = "outputs/sample_agent_run.json"
    os.makedirs(os.path.dirname(AGENT_RUN), exist_ok=True)

    prompt = [
        {"role" : "system", "content" : output_system},
        {"role" : "user", "content" : output_user_template.format(
            request=user_request,
            agent_response=agent_response
        )}
    ]

    response = call_groq(prompt=prompt)

    if os.path.exists(AGENT_RUN):
        with open(AGENT_RUN, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(json.loads(response))

    with open(AGENT_RUN, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
        print("Output Stored Successfully.")