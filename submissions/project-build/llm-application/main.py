import json
from pathlib import Path
from groq_client import run_case, build_prompt, save_output
from datetime import datetime
from prompts import (
    BLOG_INTENT_CLASSIFIER_SM,
    BLOG_INPUT_SUMMARIZATION_SM,
    BLOG_INPUT_SUMMARIZATION_EXAMPLES,
    BLOG_OUTLINE_SM,
    SEO_METADATA_SM,
    SEO_METADATA_EXAMPLES,
    BLOG_DRAFT_SM,
    QUALITY_REVIEW_SM,
    H_CONTROL_SM   
)
from validator import VALIDATION_SYSTEM_MESSAGE


def run_case_pipeline(case_id: str, user_input: str):
    print(f"\n{'='*40}")
    print(f"Running {case_id}")
    print(f"{'='*40}")

    # Step 1 — Validation
    print(f"[{case_id}] Running validation...")
    validation_messages = build_prompt(VALIDATION_SYSTEM_MESSAGE, user_input)
    validation_raw = run_case(validation_messages, temperature=0)
    save_output(f"{case_id}_validation", validation_raw)

    validation_result = json.loads(validation_raw.strip().removeprefix("```json").removesuffix("```").strip()
                                   )
    # Now it will check if the result of validation is valid 
    if not validation_result.get("is_valid"):
        print(f"[{case_id}] Validation failed:")
        for error in validation_result.get("errors", []):
            print(f"  - {error['field']}: {error['message']}")
        return

    # Step 2 — Intent 
    print(f"[{case_id}] Running intent classification...")
    intent_messages = build_prompt(BLOG_INTENT_CLASSIFIER_SM, user_input)
    intent_raw = run_case(intent_messages, temperature=0)
    save_output(f"{case_id}_intent", intent_raw)

    # Step 3 — Input Summarization using user summary
    print(f"[{case_id}] Running input summarization...")
    summary_messages = build_prompt(
        BLOG_INPUT_SUMMARIZATION_SM,
        user_input,
        examples=BLOG_INPUT_SUMMARIZATION_EXAMPLES
    )
    summary_raw = run_case(summary_messages, temperature=0)
    save_output(f"{case_id}_summary", summary_raw)

    # Step 4 — Outline using intent + summary 
    print(f"[{case_id}] Running outline generation...")
    outline_input = f"""
USER INPUT:
{user_input}

INTENT CLASSIFICATION:
{open(f"outputs/{case_id}_intent.json").read()}

BLOG SUMMARY:
{open(f"outputs/{case_id}_summary.json").read()}
    """
    outline_messages = build_prompt(BLOG_OUTLINE_SM, outline_input)
    outline_raw = run_case(outline_messages, temperature=0.2)
    save_output(f"{case_id}_outline", outline_raw)

    # Step 5 - Seo metadata using blog draft + user summary 
    print(f"[{case_id}] Running SEO metadata generation...")
    seo_input = f"""
USER INPUT:
{user_input}

BLOG SUMMARY:
{open(f"outputs/{case_id}_summary.json").read()}

BLOG OUTLINE:
{open(f"outputs/{case_id}_outline.json").read()}
    """
    seo_messages = build_prompt(SEO_METADATA_SM, seo_input, examples=SEO_METADATA_EXAMPLES)
    seo_raw = run_case(seo_messages, temperature=0)
    save_output(f"{case_id}_seo", seo_raw)

    print(f"[{case_id}] Complete — all outputs saved to outputs/")

    # Step 6 — Blog Draft using outline + intent + summary 
    print(f"[{case_id}] Running blog draft generation...")
    draft_input = f"""
USER INPUT:
{user_input}

INTENT CLASSIFICATION:
{open(f"outputs/{case_id}_intent.json").read()}

BLOG SUMMARY:
{open(f"outputs/{case_id}_summary.json").read()}

BLOG OUTLINE:
{open(f"outputs/{case_id}_outline.json").read()}
    """
    draft_messages = build_prompt(BLOG_DRAFT_SM, draft_input)
    draft_raw = run_case(draft_messages, temperature=0.4)
    save_output(f"{case_id}_draft", draft_raw)

    # Step 7 - Quality Review using input + summary + classification + blog outline + draft 
    print(f"[{case_id}] Running quality review...")
    review_input = f"""
USER INPUT:
{user_input}

INTENT CLASSIFICATION:
{open(f"outputs/{case_id}_intent.json").read()}

BLOG SUMMARY:
{open(f"outputs/{case_id}_summary.json").read()}

BLOG OUTLINE:
{open(f"outputs/{case_id}_outline.json").read()}

BLOG DRAFT:
{open(f"outputs/{case_id}_draft.json").read()}
    """
    review_messages = build_prompt(QUALITY_REVIEW_SM, review_input)
    review_raw = run_case(review_messages, temperature=0.0)
    save_output(f"{case_id}_review", review_raw)

    # Step 8 - Hallucination Check on only blog draft 
    print(f"[{case_id}] Running quality review...")
    hcheck_input = f"""
USER INPUT:
{user_input}

BLOG DRAFT:
{open(f"outputs/{case_id}_draft.json").read()}

"""
    hcheck_messages = build_prompt(H_CONTROL_SM, hcheck_input)
    hcheck_raw = run_case(hcheck_messages, temperature=0.0)
    save_output(f"{case_id}_hallucination_check", hcheck_raw)

    # Step 9 - Final Output Package (no LLM call needed)
    print(f"[{case_id}] Assembling final output package...")

    final_output = {
        "blog_intent_analysis": json.loads(open(f"outputs/{case_id}_intent.json").read()),
        "input_summary": json.loads(open(f"outputs/{case_id}_summary.json").read()),
        "blog_outline": json.loads(open(f"outputs/{case_id}_outline.json").read()),
        "final_blog": open(f"outputs/{case_id}_draft.json").read(),
        "seo_metadata": json.loads(open(f"outputs/{case_id}_seo.json").read()),
        "linkedin_post": {},
        "quality_review": json.loads(open(f"outputs/{case_id}_review.json").read()),
        "hallucination_check": json.loads(open(f"outputs/{case_id}_hallucination_check.json").read()),
        "generation_metadata": {
            "model_used": "llama-3.3-70b-versatile",
            "temperature": 0.4,
            "total_steps_completed": 8,
            "steps": ["validation", "intent", "summary", "outline", "seo", "draft", "quality_review", "hallucination_check"],
            "timestamp": str(datetime.now().isoformat())
        }
    }

    save_output(f"{case_id}_final", json.dumps(final_output))
    print(f"[{case_id}] Final output package saved.")


if __name__ == "__main__":
    print("Enter your blog details below (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    user_input = "\n".join(lines)

    run_case_pipeline("case_01", user_input)
    