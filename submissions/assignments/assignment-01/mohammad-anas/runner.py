from groq_client import call_llm
import json

def run_prompt(prompt, output_file):

    response = call_llm(prompt)

    result = json.loads(response)

    with open(output_file, 'w') as file:
        json.dump(result, file, indent=4)   

    print("Saved output to", output_file)
    return result