#Groq API client and helper functions

import os
import json
import re
from groq import Groq
from pathlib import Path

#Loading environment variables and groq API key
from dotenv import load_dotenv
load_dotenv()  

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq()
DEFAULT_MODEL = "openai/gpt-oss-120b"

def call_llm(prompt: str, model: str = DEFAULT_MODEL, temperature: float = 0) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content

def extract_json(response_text: str) -> dict | list | None:     
    try:
        return json.loads(response_text.strip())
    except json.JSONDecodeError:
        pass

    cleaned = re.sub(r"```(?:json)?", "", response_text).replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None

def save_output(filename: str, data: dict | list, output_dir: str = "outputs") -> None:
    p = Path(filename)
    if p.parent and str(p.parent) != ".":
        target_path = p
    else:
        target_path = Path(output_dir) / p.name

    target_path.parent.mkdir(parents=True, exist_ok=True)

    with target_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[ OUTPUT SAVED ]")
    return str(target_path)

def run_case(case_name: str, prompt: str, temperature: float, model: str = DEFAULT_MODEL,) -> dict:

    raw_response = call_llm(prompt, model=model, temperature=temperature)
    parsed = extract_json(raw_response)
    result = {
        "parsed_output": parsed,
    }
    return result

def run_self_consistency(case_name: str, prompt: str, result_key: str, num_runs: int = 5):
  
    from collections import Counter

    individual_answers = []
    vote_values = []

    for i in range(num_runs):
        raw = call_llm(prompt, temperature=0.3)
        parsed = extract_json(raw)

        individual_answers.append({
            "run": i + 1,
            "raw_response": raw,
            "parsed": parsed,
        })

        if parsed and result_key in parsed:
            vote_values.append(str(parsed[result_key]))

    vote_counts = Counter(vote_values)

    if vote_counts:
        final_answer, consistency_count = vote_counts.most_common(1)[0]
    else:
        final_answer, consistency_count = "UNKNOWN", 0

    return {
        "case_name": case_name,
        "individual_answers": individual_answers,
        f"{result_key}_votes": dict(vote_counts),
        f"final_{result_key}": final_answer,
        "consistency_count": consistency_count,
    }