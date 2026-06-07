import json
from pathlib import Path
from groq_client import run_case, build_prompt, save_output, parse_json_response
from datetime import datetime
from prompts import (
    TICKET_SUMMARIZATION_SM,
    TICKET_CLASSIFICATION_SM,
    TICKET_CLASSIFICATION_EXAMPLES,
    SENTIMENT_ANALYSIS_SM,
    PRIORITY_RISK_SM,
    PRIORITY_RISK_EXAMPLES,
    SENSITIVE_INFO_SM,
    ROUTING_SM,
    DRAFT_RESPONSE_SM,
    QUALITY_REVIEW_SM,
)
from validator import validate_ticket_inputs


def load(case_id: str, step: str) -> str:
    return open(f"outputs/{case_id}_{step}.json").read()


def run_ticket_pipeline(case_id: str, ticket_input: dict):
    print(f"\n{'='*40}")
    print(f"Running {case_id}")
    print(f"{'='*40}")

    ticket_str = json.dumps(ticket_input, indent=2)

    print(f"[{case_id}] Validating ticket input...")
    validation_result = validate_ticket_inputs(ticket_input)
    save_output(f"{case_id}_validation", json.dumps(validation_result))

    if not validation_result.get("is_valid"):
        print(f"[{case_id}] Validation failed:")
        for error in validation_result.get("errors", []):
            print(f"  - {error['field']}: {error['message']}")
        return

    print(f"[{case_id}] Running ticket summarization...")
    summary_messages = build_prompt(TICKET_SUMMARIZATION_SM, ticket_str)
    summary_raw = run_case(summary_messages, temperature=0)
    save_output(f"{case_id}_summary", summary_raw)

    print(f"[{case_id}] Running ticket classification...")
    classification_messages = build_prompt(
        TICKET_CLASSIFICATION_SM,
        ticket_str,
        examples=TICKET_CLASSIFICATION_EXAMPLES
    )
    classification_raw = run_case(classification_messages, temperature=0)
    save_output(f"{case_id}_classification", classification_raw)

    print(f"[{case_id}] Running sentiment analysis...")
    sentiment_messages = build_prompt(SENTIMENT_ANALYSIS_SM, ticket_str)
    sentiment_raw = run_case(sentiment_messages, temperature=0)
    save_output(f"{case_id}_sentiment", sentiment_raw)

    print(f"[{case_id}] Running priority and escalation risk detection...")
    priority_input = f"""
TICKET INPUT:
{ticket_str}

CLASSIFICATION:
{load(case_id, 'classification')}

SENTIMENT:
{load(case_id, 'sentiment')}
    """
    priority_messages = build_prompt(
        PRIORITY_RISK_SM,
        priority_input,
        examples=PRIORITY_RISK_EXAMPLES
    )
    priority_raw = run_case(priority_messages, temperature=0)
    save_output(f"{case_id}_priority", priority_raw)

    print(f"[{case_id}] Running sensitive information detection...")
    sensitive_messages = build_prompt(SENSITIVE_INFO_SM, ticket_str)
    sensitive_raw = run_case(sensitive_messages, temperature=0)
    save_output(f"{case_id}_sensitive", sensitive_raw)

    print(f"[{case_id}] Running routing recommendation...")
    routing_input = f"""
TICKET INPUT:
{ticket_str}

CLASSIFICATION:
{load(case_id, 'classification')}

PRIORITY AND RISK:
{load(case_id, 'priority')}

SENSITIVE INFO:
{load(case_id, 'sensitive')}
    """
    routing_messages = build_prompt(ROUTING_SM, routing_input)
    routing_raw = run_case(routing_messages, temperature=0)
    save_output(f"{case_id}_routing", routing_raw)

    print(f"[{case_id}] Running draft response generation...")
    draft_input = f"""
TICKET INPUT:
{ticket_str}

TICKET SUMMARY:
{load(case_id, 'summary')}

CLASSIFICATION:
{load(case_id, 'classification')}

PRIORITY AND RISK:
{load(case_id, 'priority')}

ROUTING:
{load(case_id, 'routing')}
    """
    draft_messages = build_prompt(DRAFT_RESPONSE_SM, draft_input)
    draft_raw = run_case(draft_messages, temperature=0.2)
    save_output(f"{case_id}_draft", draft_raw)

    print(f"[{case_id}] Running response quality review...")
    review_input = f"""
TICKET INPUT:
{ticket_str}

TICKET SUMMARY:
{load(case_id, 'summary')}

DRAFT RESPONSE:
{load(case_id, 'draft')}
    """
    review_messages = build_prompt(QUALITY_REVIEW_SM, review_input)
    review_raw = run_case(review_messages, temperature=0)
    save_output(f"{case_id}_review", review_raw)

    print(f"[{case_id}] Assembling final ticket intelligence package...")

    final_output = {
        "ticket_summary":           parse_json_response(load(case_id, "summary")),
        "classification":           parse_json_response(load(case_id, "classification")),
        "sentiment_analysis":       parse_json_response(load(case_id, "sentiment")),
        "priority_and_risk":        parse_json_response(load(case_id, "priority")),
        "sensitive_information_check": parse_json_response(load(case_id, "sensitive")),
        "routing_recommendation":   parse_json_response(load(case_id, "routing")),
        "draft_customer_response":  parse_json_response(load(case_id, "draft")),
        "response_quality_review":  parse_json_response(load(case_id, "review")),
        "generation_metadata": {
            "model_used": "llama-3.3-70b-versatile",
            "temperature": 0.2,
            "total_steps_completed": 8,
            "steps": [
                "summarization", "classification", "sentiment",
                "priority_risk", "sensitive_info", "routing",
                "draft_response", "quality_review"
            ],
            "timestamp": datetime.now().isoformat()
        }
    }

    save_output(f"{case_id}_final", json.dumps(final_output, indent=2))
    print(f"[{case_id}] Final package saved to outputs/{case_id}_final.json")


if __name__ == "__main__":
    print("Paste your ticket input as JSON (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    raw_input = "\n".join(lines)

    try:
        ticket_input = json.loads(raw_input)
    except json.JSONDecodeError:
        print("Invalid JSON input. Please paste a valid ticket JSON object.")
        exit(1)

    run_ticket_pipeline("case_01", ticket_input)
