"""
Reusable Groq API client and helper functions for prompt engineering evaluation.
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# load API KEY
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")

# Initialize client securely
client = Groq()

def call_llm(system_prompt, user_prompt, model="openai/gpt-oss-120b", temperature=0.2):
    """
    Call Groq LLM with system + user prompts.
    Returns raw response text.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def extract_json(response_text):
    """
    Attempt to parse JSON from model response.
    If invalid, print warning and return None.
    """
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        print("[WARNING] Response is not valid JSON.")
        return None


def save_output(filename, data):
    try:
        # Normalize non-breaking hyphens to regular hyphens
        def normalize(obj):
            if isinstance(obj, str):
                return obj.replace("\u2011", "-")
            if isinstance(obj, list):
                return [normalize(x) for x in obj]
            if isinstance(obj, dict):
                return {k: normalize(v) for k, v in obj.items()}
            return obj

        normalized_data = normalize(data)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(normalized_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[WARNING] Could not save file {filename}: {e}")


def run_case(case_name, system_prompt, user_prompt, temperature=0.2, output_dir="outputs"):
    """
    Run a single case: call LLM with system + user prompts,
    parse JSON, save result.
    Returns structured result or None.
    """
    response_text = call_llm(system_prompt, user_prompt, temperature=temperature)
    result = extract_json(response_text)
    if result:
        save_output(os.path.join(output_dir, f"{case_name}.json"), result)
    return result