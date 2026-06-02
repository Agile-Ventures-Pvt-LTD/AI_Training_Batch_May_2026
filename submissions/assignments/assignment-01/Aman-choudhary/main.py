from groq_client import call_llm
import json
import os

from prompts import (
    zero_shot_prompt,
    zero_shot_executive_prompt,
    few_shot_ticket_prompt,
    few_shot_api_prompt,
    cot_roi_prompt,
    cot_ml_prompt,
    llm_judge_support_prompt,
    llm_judge_python_prompt,
    self_consistency_policy_prompt,
    self_consistency_security_prompt,
    tree_of_thought_prompt,
    tree_of_thought_architecture_prompt,
    rephrase_prompt,
    rephrase_technical_prompt
)

# =========================================================
# JSON EXTRACTION
# =========================================================

def extract_json(response_text):

    try:

        cleaned = response_text.strip()

        # Remove markdown JSON formatting
        if cleaned.startswith("```json"):

            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "")
            cleaned = cleaned.strip()

        parsed = json.loads(cleaned)

        return parsed

    except json.JSONDecodeError as e:

        print("\nJSON Parsing Error:")
        print(e)

        return {
            "error": "Invalid JSON response",
            "raw_response": response_text
        }


# =========================================================
# SAVE OUTPUT
# =========================================================

def save_output(filename, case_name, data):

    try:

        existing_data = {}

        # Load existing JSON file
        if os.path.exists(filename):

            with open(filename, "r", encoding="utf-8") as file:

                try:

                    existing_data = json.load(file)

                except json.JSONDecodeError:

                    existing_data = {}

        # Add new case result
        existing_data[case_name] = data

        # Rewrite clean JSON structure
        with open(filename, "w", encoding="utf-8") as file:

            json.dump(existing_data, file, indent=4)

        print(f"\nOutput saved successfully -> {filename}")

    except Exception as e:

        print("\nFile Saving Error:")
        print(e)


# =========================================================
# GENERIC CASE RUNNER
# =========================================================

def run_case(
    case_name,
    prompt,
    output_file,
    temperature=0.2
):

    print(f"\n{'=' * 70}")
    print(f"RUNNING: {case_name}")
    print(f"{'=' * 70}\n")

    try:

        response = call_llm(
            prompt,
            temperature=temperature
        )

        if not response:

            raise ValueError(
                "Empty response received from model."
            )

        parsed_response = extract_json(response)

        print(
            json.dumps(
                parsed_response,
                indent=2
            )
        )

        save_output(
            output_file,
            case_name,
            parsed_response
        )

    except ValueError as ve:

        print("\nValue Error:")
        print(ve)

    except FileNotFoundError as fe:

        print("\nFile Not Found Error:")
        print(fe)

    except Exception as e:

        print("\nUnexpected Error:")
        print(e)


# =========================================================
# SELF CONSISTENCY RUNNER
# =========================================================

def run_self_consistency(
    case_name,
    prompt,
    output_file,
    runs=5,
    temperature=0.7
):

    print(f"\n{'=' * 70}")
    print(f"RUNNING SELF CONSISTENCY: {case_name}")
    print(f"{'=' * 70}\n")

    responses = []

    try:

        for i in range(runs):

            print(f"\nRun {i+1}")

            response = call_llm(
                prompt,
                temperature=temperature
            )

            if not response:

                raise ValueError(
                    f"Empty response in run {i+1}"
                )

            parsed = extract_json(response)

            responses.append(parsed)

        print(
            json.dumps(
                responses,
                indent=2
            )
        )

        save_output(
            output_file,
            case_name,
            responses
        )

    except Exception as e:

        print("\nSelf Consistency Error:")
        print(e)


# =========================================================
# OUTPUT DIRECTORY CHECK
# =========================================================

try:

    if not os.path.exists("outputs"):

        os.makedirs("outputs")

except Exception as e:

    print("\nDirectory Creation Error:")
    print(e)


# =========================================================
# ZERO SHOT CASE 1.1
# =========================================================

run_case(
    case_name="Zero Shot Case 1.1 - Vendor Risk Classification",
    prompt=zero_shot_prompt,
    output_file="outputs/zero_shot_outputs.json",
    temperature=0.2
)

# =========================================================
# ZERO SHOT CASE 1.2
# =========================================================

run_case(
    case_name="Zero Shot Case 1.2 - Executive Decision Memo",
    prompt=zero_shot_executive_prompt,
    output_file="outputs/zero_shot_outputs.json",
    temperature=0.2
)

# =========================================================
# FEW SHOT CASE 2.1
# =========================================================

run_case(
    case_name="Few Shot Case 2.1 - Ticket Classification",
    prompt=few_shot_ticket_prompt,
    output_file="outputs/few_shot_outputs.json",
    temperature=0.3
)

# =========================================================
# FEW SHOT CASE 2.2
# =========================================================

run_case(
    case_name="Few Shot Case 2.2 - API Contract Generation",
    prompt=few_shot_api_prompt,
    output_file="outputs/few_shot_outputs.json",
    temperature=0.3
)

# =========================================================
# CHAIN OF THOUGHT CASE 3.1
# =========================================================

run_case(
    case_name="CoT Case 3.1 - ROI Analysis",
    prompt=cot_roi_prompt,
    output_file="outputs/cot_outputs.json",
    temperature=0.2
)

# =========================================================
# CHAIN OF THOUGHT CASE 3.2
# =========================================================

run_case(
    case_name="CoT Case 3.2 - ML Root Cause Analysis",
    prompt=cot_ml_prompt,
    output_file="outputs/cot_outputs.json",
    temperature=0.2
)

# =========================================================
# LLM JUDGE CASE 4.1
# =========================================================

run_case(
    case_name="LLM Judge Case 4.1 - Support Evaluation",
    prompt=llm_judge_support_prompt,
    output_file="outputs/llm_judge_outputs.json",
    temperature=0.1
)

# =========================================================
# LLM JUDGE CASE 4.2
# =========================================================

run_case(
    case_name="LLM Judge Case 4.2 - Python Explanation Evaluation",
    prompt=llm_judge_python_prompt,
    output_file="outputs/llm_judge_outputs.json",
    temperature=0.1
)

# =========================================================
# SELF CONSISTENCY CASE 5.1
# =========================================================

run_self_consistency(
    case_name="Self Consistency Case 5.1",
    prompt=self_consistency_policy_prompt,
    output_file="outputs/self_consistency_outputs.json",
    runs=5,
    temperature=0.7
)

# =========================================================
# SELF CONSISTENCY CASE 5.2
# =========================================================

run_self_consistency(
    case_name="Self Consistency Case 5.2",
    prompt=self_consistency_security_prompt,
    output_file="outputs/self_consistency_outputs.json",
    runs=5,
    temperature=0.7
)

# =========================================================
# TREE OF THOUGHT CASE 6.1
# =========================================================

run_case(
    case_name="Tree of Thought Case 6.1",
    prompt=tree_of_thought_prompt,
    output_file="outputs/tree_of_thought_outputs.json",
    temperature=0.5
)

# =========================================================
# TREE OF THOUGHT CASE 6.2
# =========================================================

run_case(
    case_name="Tree of Thought Case 6.2 - Architecture Selection",
    prompt=tree_of_thought_architecture_prompt,
    output_file="outputs/tree_of_thought_outputs.json",
    temperature=0.5
)

# =========================================================
# REPHRASE AND RESPOND CASE 7.1
# =========================================================

run_case(
    case_name="Rephrase and Respond Case 7.1",
    prompt=rephrase_prompt,
    output_file="outputs/rephrase_respond_outputs.json",
    temperature=0.3
)

# =========================================================
# REPHRASE AND RESPOND CASE 7.2
# =========================================================

run_case(
    case_name="Rephrase and Respond Case 7.2 - Technical Requirement",
    prompt=rephrase_technical_prompt,
    output_file="outputs/rephrase_respond_outputs.json",
    temperature=0.3
)

print("\nALL EVALUATION CASES COMPLETED SUCCESSFULLY\n")